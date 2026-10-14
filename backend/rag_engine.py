"""
RAG (Retrieval-Augmented Generation) Engine
Uses ChromaDB vector store + Google Gemini for legal Q&A
"""

import os
from typing import List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

try:
    from langchain_community.vectorstores import Chroma
    HAS_CHROMA = True
except (ImportError, Exception):
    Chroma = None
    HAS_CHROMA = False

from knowledge_base import build_documents

load_dotenv()

if os.environ.get("VERCEL"):
    CHROMA_DB_PATH = os.path.join("/tmp", "chroma_db")
else:
    CHROMA_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")


class InMemoryLegalRetriever:
    """Lightweight in-memory retriever for serverless/Vercel environments without ChromaDB."""

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
   - ### ⚠️ Important Disclaimer (brief note to consult an advocate)
5. Use standard markdown headers (`### `) for main categories.
6. Emphasize key terms with bold text and use bullet points for lists.

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


class LegalRAGEngine:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0.3,
            max_output_tokens=2048,
        )

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=self.api_key,
        )

        self.vectorstore: Optional[Chroma] = None
        self.retriever = None
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """Initialize ChromaDB or fallback to in-memory retriever for Vercel/serverless."""
        documents = build_documents()

        if not HAS_CHROMA or Chroma is None:
            print("[INFO] ChromaDB not available. Using high-efficiency in-memory legal retriever...")
            self.vectorstore = None
            self.retriever = InMemoryLegalRetriever(documents)
            return

        try:
            os.makedirs(CHROMA_DB_PATH, exist_ok=True)
            # Check if DB already exists
            if os.path.exists(os.path.join(CHROMA_DB_PATH, "chroma.sqlite3")):
                print("[INFO] Loading existing vector store...")
                self.vectorstore = Chroma(
                    persist_directory=CHROMA_DB_PATH,
                    embedding_function=self.embeddings,
                    collection_name="indian_legal_kb"
                )
            else:
                print("[INFO] Building new vector store from legal knowledge base...")
                self.vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    persist_directory=CHROMA_DB_PATH,
                    collection_name="indian_legal_kb"
                )
                print(f"[INFO] Vector store built with {len(documents)} documents")

            self.retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
        except Exception as e:
            print(f"[WARN] ChromaDB initialization failed: {e}. Falling back to in-memory retriever...")
            self.vectorstore = None
            self.retriever = InMemoryLegalRetriever(documents)

    def refresh_knowledge_base(self):
        """Rebuild the vector store from scratch."""
        import shutil
        if os.path.exists(CHROMA_DB_PATH):
            shutil.rmtree(CHROMA_DB_PATH)
        self._initialize_vectorstore()

    def _format_docs(self, docs: List[Document]) -> str:
        """Format retrieved documents into context string."""
        formatted = []
        for i, doc in enumerate(docs, 1):
            formatted.append(
                f"[Source {i}: {doc.metadata.get('source', 'Unknown')}]\n"
                f"Category: {doc.metadata.get('category', 'General')}\n"
                f"{doc.page_content}"
            )
        return "\n\n---\n\n".join(formatted)

    def get_relevant_sources(self, query: str) -> List[dict]:
        """Get relevant documents for a query without generating a response."""
        docs = self.retriever.invoke(query)
        return [
            {
                "source": doc.metadata.get("source", "Unknown"),
                "category": doc.metadata.get("category", "General"),
                "excerpt": doc.page_content[:200] + "..."
            }
            for doc in docs
        ]

    def answer(self, question: str, chat_history: str = "", user_id: str = "default_user", language: str = "en", level: str = "new") -> dict:
        """
        Generate a legal answer using RAG with continuous learning memory, multilingual output, and level-adapted framing.
        Returns dict with 'answer' and 'sources'.
        """
        from memory_learning import get_learning_memory
        memory = get_learning_memory()

        target_lang_str = LANGUAGE_NAMES.get(language, "English")

        level_descriptions = {
            "new": "New / Beginner (Citizen with no prior legal exposure. Use plain everyday words, simple analogies, eliminate complex legal jargon, emphasize fundamental practical rights and immediate actions.)",
            "intermediate": "Intermediate (Practical knowledge seeker. Provide clear statutory rights, standard legal procedures, filing requirements, and realistic expectations.)",
            "expert": "Expert / Legal Practitioner (Advanced legal framing. Emphasize statutory definitions, sections, procedural nuances under BNSS/CPC, jurisdictional nuances, case precedents, and precise legal remedies.)"
        }
        level_desc = level_descriptions.get(level.lower(), level_descriptions["new"])

        # Retrieve relevant docs
        relevant_docs = self.retriever.invoke(question)
        context = self._format_docs(relevant_docs)

        # Retrieve user covered topics and learned insights
        covered_topics = memory.get_user_topics_context(user_id)
        learned_insights = memory.get_learned_insights()

        # Build prompt
        prompt = ChatPromptTemplate.from_template(LEGAL_SYSTEM_PROMPT)

        # Build chain
        chain = prompt | self.llm | StrOutputParser()

        # Generate answer
        answer = chain.invoke({
            "context": context,
            "chat_history": chat_history,
            "covered_topics": covered_topics,
            "learned_insights": learned_insights,
            "complexity_level_description": level_desc,
            "target_language": target_lang_str,
            "question": question
        })

        # Save topic to learning memory so it won't repeat
        memory.record_topic(question, answer, user_id)

        # Compile sources
        sources = [
            {
                "source": doc.metadata.get("source", "Unknown"),
                "category": doc.metadata.get("category", "General"),
            }
            for doc in relevant_docs
        ]

        return {
            "answer": answer,
            "sources": sources
        }


# Singleton instance
_engine: Optional[LegalRAGEngine] = None


def get_rag_engine() -> LegalRAGEngine:
    """Get or create the RAG engine singleton."""
    global _engine
    if _engine is None:
        _engine = LegalRAGEngine()
    return _engine
