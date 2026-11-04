"""
RAG (Retrieval-Augmented Generation) Engine
Uses a lightweight in-memory retriever + Google Gemini API directly.
No langchain/chromadb — fits within Vercel's 500 MB function bundle limit.
"""

import os
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

try:
    # Only attempt langchain imports in non-Vercel local dev
    if not os.environ.get("VERCEL"):
        from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
        from langchain_core.documents import Document
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        from langchain_community.vectorstores import Chroma
        HAS_LANGCHAIN = True
        HAS_CHROMA = True
    else:
        raise ImportError("Vercel env — skip langchain")
except Exception:
    HAS_LANGCHAIN = False
    HAS_CHROMA = False
    # Minimal Document stand-in
    class Document:  # type: ignore[no-redef]
        def __init__(self, page_content: str, metadata: dict = None):
            self.page_content = page_content
            self.metadata = metadata or {}

from knowledge_base import build_documents

load_dotenv()

CHROMA_DB_PATH = os.path.join("/tmp", "chroma_db") if os.environ.get("VERCEL") else \
    os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")

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

LEGAL_SYSTEM_PROMPT = """You are VakilBot, an intelligent AI legal assistant specializing in Indian law. You continuously adapt and learn to provide deep, non-repetitive, and actionable guidance based on publicly available Indian laws.

USER EXPERIENCE LEVEL: {complexity_level_description}

LANGUAGE REQUIREMENT:
You MUST respond entirely in the requested TARGET LANGUAGE: {target_language}.
Translate all explanations, headings, and legal concepts clearly into {target_language} while preserving exact legal section numbers, act names (e.g. BNS, IPC, BNSS, Constitution Articles), and helpline numbers.

CRITICAL INTELLIGENCE & ANTI-REPETITION RULES:
1. Frame your answer according to the selected USER EXPERIENCE LEVEL:
   - For 'New / Beginner': Use simple everyday analogies, eliminate confusing legalese, explain basics clearly as if talking to a common citizen who has never visited a court.
   - For 'Intermediate': Provide balanced practical guidance, actionable statutory rights, procedural steps, and standard legal recourse.
   - For 'Expert': Use precise legal jurisprudence, statutory definitions, jurisdictional authorities (High Court, Supreme Court, Tribunals), limitation periods, procedural requisites under BNSS/CPC, and landmark case precedents.
2. DO NOT repeat the same explanations, introductions, or basic boilerplate that was already stated in the CONVERSATION HISTORY or PREVIOUS USER TOPICS.
3. If the user is asking a follow-up or a related question, build upon what has already been explained. Deepen the explanation, offer tactical nuances, court precedents, exceptions, and procedural depth instead of repeating general introductions.
4. Structure your response with clean, clearly separated visual sections so the user can immediately distinguish between topics:
   - ### 📌 Summary / Overview
   - ### ⚖️ Applicable Laws & Sections
   - ### 🛡️ Your Rights & Protections
   - ### 📝 Practical Steps You Can Take
   - ### 📞 Important Helplines & Portals (if applicable)
   - ### ⚠️ Important Disclaimer
5. Use standard markdown headers (`### `) for main categories.
6. Emphasize key terms with bold text and use bullet points for lists.
7. ALWAYS end with: "⚠️ **Disclaimer**: This is general legal information, not legal advice. Please consult a qualified advocate for your specific situation. Free legal aid: [NALSA](https://nalsa.gov.in) | Helpline: 15100"

LEARNED COLLECTIVE INSIGHTS:
{learned_insights}

PREVIOUSLY COVERED TOPICS FOR THIS USER:
{covered_topics}

LEGAL CONTEXT FROM KNOWLEDGE BASE:
{context}

CONVERSATION HISTORY:
{chat_history}

USER QUESTION: {question}

Provide an insightful, nuanced response in {target_language} following the structured format without repeating previous statements:"""


class InMemoryLegalRetriever:
    """Lightweight in-memory retriever — no external dependencies."""

    def __init__(self, documents: List):
        self.documents = documents

    def invoke(self, query: str) -> List:
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


class LegalRAGEngine:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=self.api_key)
        self._model = genai.GenerativeModel("gemini-2.5-flash")

        self.vectorstore = None
        self.retriever = None
        self._initialize_retriever()

    def _initialize_retriever(self):
        """Always use in-memory retriever on Vercel; optionally ChromaDB locally."""
        documents = build_documents()

        if HAS_CHROMA and not os.environ.get("VERCEL"):
            try:
                from langchain_google_genai import GoogleGenerativeAIEmbeddings
                from langchain_community.vectorstores import Chroma as ChromaStore
                embeddings = GoogleGenerativeAIEmbeddings(
                    model="models/gemini-embedding-001",
                    google_api_key=self.api_key,
                )
                os.makedirs(CHROMA_DB_PATH, exist_ok=True)
                if os.path.exists(os.path.join(CHROMA_DB_PATH, "chroma.sqlite3")):
                    print("[INFO] Loading existing ChromaDB vector store...")
                    self.vectorstore = ChromaStore(
                        persist_directory=CHROMA_DB_PATH,
                        embedding_function=embeddings,
                        collection_name="indian_legal_kb"
                    )
                else:
                    print("[INFO] Building new ChromaDB vector store...")
                    self.vectorstore = ChromaStore.from_documents(
                        documents=documents,
                        embedding=embeddings,
                        persist_directory=CHROMA_DB_PATH,
                        collection_name="indian_legal_kb"
                    )
                self.retriever = self.vectorstore.as_retriever(
                    search_type="similarity", search_kwargs={"k": 4}
                )
                print(f"[INFO] ChromaDB ready with {len(documents)} documents")
                return
            except Exception as e:
                print(f"[WARN] ChromaDB failed: {e}. Falling back to in-memory retriever.")

        print("[INFO] Using lightweight in-memory legal retriever.")
        self.retriever = InMemoryLegalRetriever(documents)

    def _format_docs(self, docs: List) -> str:
        formatted = []
        for i, doc in enumerate(docs, 1):
            formatted.append(
                f"[Source {i}: {doc.metadata.get('source', 'Unknown')}]\n"
                f"Category: {doc.metadata.get('category', 'General')}\n"
                f"{doc.page_content}"
            )
        return "\n\n---\n\n".join(formatted)

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
        """Generate a legal answer using RAG + Gemini API directly."""
        from memory_learning import get_learning_memory
        memory = get_learning_memory()

        target_lang_str = LANGUAGE_NAMES.get(language, "English")

        level_descriptions = {
            "new": "New / Beginner (Citizen with no prior legal exposure. Use plain everyday words, simple analogies, eliminate complex legal jargon, emphasize fundamental practical rights and immediate actions.)",
            "intermediate": "Intermediate (Practical knowledge seeker. Provide clear statutory rights, standard legal procedures, filing requirements, and realistic expectations.)",
            "expert": "Expert / Legal Practitioner (Advanced legal framing. Emphasize statutory definitions, sections, procedural nuances under BNSS/CPC, jurisdictional nuances, case precedents, and precise legal remedies.)"
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

        response = self._model.generate_content(prompt)
        answer_text = response.text

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
        if os.path.exists(CHROMA_DB_PATH):
            shutil.rmtree(CHROMA_DB_PATH)
        self._initialize_retriever()


# Singleton
_engine: Optional[LegalRAGEngine] = None


def get_rag_engine() -> LegalRAGEngine:
    global _engine
    if _engine is None:
        _engine = LegalRAGEngine()
    return _engine
