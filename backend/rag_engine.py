"""
RAG Engine — Pure HTTP Gemini API client, no heavy SDKs.
Uses httpx to call the Gemini REST API directly.
Runs entirely within Vercel's 500 MB function bundle limit.
"""

import os
import httpx
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Minimal Document class (no langchain dependency)
# ---------------------------------------------------------------------------

class Document:
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata = metadata or {}


# ---------------------------------------------------------------------------
# Language mapping
# ---------------------------------------------------------------------------

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi (हिंदी)",
    "ta": "Tamil (தமிழ்)",
    "te": "Telugu (తెలుగు)",
    "bn": "Bengali (বাংলা)",
    "mr": "Marathi (मराठी)",
    "gu": "Gujarati (ગુજરાતી)",
    "kn": "Kannada (ಕನ್ನಡ)",
    "ml": "Malayalam (മലയാളം)",
    "pa": "Punjabi (ਪੰਜਾਬੀ)",
    "es": "Spanish (Español)",
    "fr": "French (Français)",
    "de": "German (Deutsch)",
    "ar": "Arabic (العربية)",
    "ru": "Russian (Русский)",
    "zh": "Mandarin Chinese (中文)"
}

# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------

LEGAL_SYSTEM_PROMPT = """You are VakilBot, an intelligent AI legal assistant specializing in Indian law. You continuously adapt and learn to provide deep, non-repetitive, and actionable guidance based on publicly available Indian laws.

USER EXPERIENCE LEVEL: {complexity_level_description}

LANGUAGE REQUIREMENT:
You MUST respond entirely in the requested TARGET LANGUAGE: {target_language}.
Translate all explanations, headings, and legal concepts clearly into {target_language} while preserving exact legal section numbers, act names (e.g. BNS, IPC, BNSS, Constitution Articles), and helpline numbers.

CRITICAL INTELLIGENCE & ANTI-REPETITION RULES:
1. Frame your answer according to the selected USER EXPERIENCE LEVEL.
2. DO NOT repeat the same explanations already stated in CONVERSATION HISTORY.
3. Build upon previous context if the user asks follow-up questions.
4. Structure your response:
   - ### 📌 Summary / Overview
   - ### ⚖️ Applicable Laws & Sections
   - ### 🛡️ Your Rights & Protections
   - ### 📝 Practical Steps You Can Take
   - ### 📞 Important Helplines & Portals (if applicable)
   - ### ⚠️ Important Disclaimer
5. Use markdown headers, bold key terms, and bullet points.
6. ALWAYS end with: "⚠️ **Disclaimer**: This is general legal information, not legal advice. Please consult a qualified advocate for your specific situation. Free legal aid: [NALSA](https://nalsa.gov.in) | Helpline: 15100"

LEARNED COLLECTIVE INSIGHTS:
{learned_insights}

PREVIOUSLY COVERED TOPICS FOR THIS USER:
{covered_topics}

LEGAL CONTEXT FROM KNOWLEDGE BASE:
{context}

CONVERSATION HISTORY:
{chat_history}

USER QUESTION: {question}

Provide an insightful, nuanced response in {target_language}:"""

# ---------------------------------------------------------------------------
# In-memory keyword retriever
# ---------------------------------------------------------------------------

class InMemoryLegalRetriever:
    """Fast keyword-score retriever — zero external dependencies."""

    def __init__(self, documents: List[Document]):
        self.documents = documents

    def invoke(self, query: str) -> List[Document]:
        query_words = set(query.lower().split())
        scored = []
        for doc in self.documents:
            content_lower = doc.page_content.lower()
            category = doc.metadata.get("category", "").lower()
            tags = [t.lower() for t in doc.metadata.get("tags", [])]
            score = 0
            for w in query_words:
                if len(w) <= 2:
                    continue
                if w in content_lower:
                    score += 2
                if w in category:
                    score += 4
                for t in tags:
                    if w in t:
                        score += 5
            scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:4]]

# ---------------------------------------------------------------------------
# Gemini REST API client (no SDK)
# ---------------------------------------------------------------------------

GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
GEMINI_MODEL = "gemini-2.5-flash"


def _call_gemini(api_key: str, prompt: str) -> str:
    """Call Gemini generateContent REST endpoint directly."""
    url = f"{GEMINI_API_BASE}/{GEMINI_MODEL}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2048,
        }
    }
    with httpx.Client(timeout=60.0) as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        # Extract text from the first candidate
        return data["candidates"][0]["content"]["parts"][0]["text"]


# ---------------------------------------------------------------------------
# RAG Engine
# ---------------------------------------------------------------------------

class LegalRAGEngine:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        self.vectorstore = None
        self.retriever = None
        self._initialize_retriever()

    def _initialize_retriever(self):
        """Always use in-memory retriever on Vercel; ChromaDB optionally in local dev."""
        from knowledge_base import build_documents
        documents = build_documents()

        # Try ChromaDB + langchain only in local dev (not on Vercel)
        if not os.environ.get("VERCEL"):
            try:
                from langchain_google_genai import GoogleGenerativeAIEmbeddings  # type: ignore
                from langchain_community.vectorstores import Chroma as ChromaStore  # type: ignore
                embeddings = GoogleGenerativeAIEmbeddings(
                    model="models/gemini-embedding-001",
                    google_api_key=self.api_key,
                )
                chroma_path = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
                os.makedirs(chroma_path, exist_ok=True)
                db_file = os.path.join(chroma_path, "chroma.sqlite3")
                if os.path.exists(db_file):
                    print("[INFO] Loading existing ChromaDB...")
                    self.vectorstore = ChromaStore(
                        persist_directory=chroma_path,
                        embedding_function=embeddings,
                        collection_name="indian_legal_kb"
                    )
                else:
                    print("[INFO] Building ChromaDB from knowledge base...")
                    self.vectorstore = ChromaStore.from_documents(
                        documents=documents,
                        embedding=embeddings,
                        persist_directory=chroma_path,
                        collection_name="indian_legal_kb"
                    )
                self.retriever = self.vectorstore.as_retriever(
                    search_type="similarity", search_kwargs={"k": 4}
                )
                print(f"[INFO] ChromaDB ready ({len(documents)} docs)")
                return
            except Exception as e:
                print(f"[WARN] ChromaDB unavailable: {e}. Using in-memory retriever.")

        print("[INFO] Using lightweight in-memory legal retriever.")
        self.retriever = InMemoryLegalRetriever(documents)

    def _format_docs(self, docs: List[Document]) -> str:
        parts = []
        for i, doc in enumerate(docs, 1):
            parts.append(
                f"[Source {i}: {doc.metadata.get('source', 'Unknown')}]\n"
                f"Category: {doc.metadata.get('category', 'General')}\n"
                f"{doc.page_content}"
            )
        return "\n\n---\n\n".join(parts)

    def get_relevant_sources(self, query: str) -> List[dict]:
        docs = self.retriever.invoke(query)
        return [
            {
                "source": doc.metadata.get("source", "Unknown"),
                "category": doc.metadata.get("category", "General"),
                "excerpt": doc.page_content[:200] + "..."
            }
            for doc in docs
        ]

    def answer(self, question: str, chat_history: str = "", user_id: str = "default_user",
               language: str = "en", level: str = "new") -> dict:
        """Generate a legal answer using RAG + Gemini REST API."""
        from memory_learning import get_learning_memory
        memory = get_learning_memory()

        target_lang_str = LANGUAGE_NAMES.get(language, "English")
        level_descriptions = {
            "new": "New / Beginner — use plain everyday words, simple analogies, eliminate legal jargon.",
            "intermediate": "Intermediate — clear statutory rights, standard procedures, realistic expectations.",
            "expert": "Expert — precise legal jurisprudence, sections, BNSS/CPC procedures, case precedents."
        }
        level_desc = level_descriptions.get(level.lower(), level_descriptions["new"])

        relevant_docs = self.retriever.invoke(question)
        context = self._format_docs(relevant_docs)
        covered_topics = memory.get_user_topics_context(user_id)
        learned_insights = memory.get_learned_insights()

        prompt = LEGAL_SYSTEM_PROMPT.format(
            complexity_level_description=level_desc,
            target_language=target_lang_str,
            learned_insights=learned_insights,
            covered_topics=covered_topics,
            context=context,
            chat_history=chat_history,
            question=question
        )

        answer_text = _call_gemini(self.api_key, prompt)
        memory.record_topic(question, answer_text, user_id)

        sources = [
            {
                "source": doc.metadata.get("source", "Unknown"),
                "category": doc.metadata.get("category", "General"),
            }
            for doc in relevant_docs
        ]

        return {"answer": answer_text, "sources": sources}

    def refresh_knowledge_base(self):
        """Rebuild the retriever from scratch."""
        import shutil
        chroma_path = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
        if os.path.exists(chroma_path):
            shutil.rmtree(chroma_path)
        self._initialize_retriever()


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------

_engine: Optional[LegalRAGEngine] = None


def get_rag_engine() -> LegalRAGEngine:
    global _engine
    if _engine is None:
        _engine = LegalRAGEngine()
    return _engine
