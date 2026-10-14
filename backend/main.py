"""
Legal Help Bot - FastAPI Backend
Indian Legal Q&A System with RAG + Google Gemini
"""

import os
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="VakilBot - Indian Legal Help Bot",
    description="AI-powered legal assistant for Indian citizens using publicly available legal information",
    version="1.0.0"
)

# ─── CORS ────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Serve frontend static files ─────────────────────────────────────────────

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


# ─── Models ──────────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []
    user_id: Optional[str] = "default_user"
    target_language: Optional[str] = "en"  # "en", "hi", "ta", "te", etc.
    complexity_level: Optional[str] = "new"  # "new", "intermediate", "expert"


class FeedbackRequest(BaseModel):
    query: str
    answer: str
    feedback: str  # "thumbs_up" or "thumbs_down"
    notes: Optional[str] = ""
    user_id: Optional[str] = "default_user"


class SourceInfo(BaseModel):
    source: str
    category: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceInfo]
    response_time_ms: int


class HealthResponse(BaseModel):
    status: str
    model: str
    knowledge_base_ready: bool
    version: str


# ─── RAG Engine (lazy loaded) ────────────────────────────────────────────────

_rag_engine = None


def get_engine():
    global _rag_engine
    if _rag_engine is None:
        from rag_engine import get_rag_engine
        _rag_engine = get_rag_engine()
    return _rag_engine


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/", response_class=FileResponse)
async def serve_frontend():
    """Serve the frontend HTML."""
    candidates = [
        os.path.join(FRONTEND_DIR, "index.html"),
        os.path.join(os.getcwd(), "frontend", "index.html"),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "frontend", "index.html")),
    ]
    for p in candidates:
        if os.path.exists(p):
            return FileResponse(p)
    return {"message": "VakilBot API is running. Frontend not found."}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        engine = get_engine()
        return HealthResponse(
            status="healthy",
            model="gemini-1.5-flash",
            knowledge_base_ready=engine.retriever is not None,
            version="1.0.0"
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main legal Q&A endpoint.
    Accepts a user message and chat history, returns legal advice with sources.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    if len(request.message) > 2000:
        raise HTTPException(status_code=400, detail="Message too long (max 2000 characters)")

    try:
        engine = get_engine()

        # Format chat history for context
        history_text = ""
        if request.history:
            recent_history = request.history[-6:]  # Last 3 exchanges
            history_lines = []
            for msg in recent_history:
                role = "User" if msg.role == "user" else "Assistant"
                history_lines.append(f"{role}: {msg.content[:300]}")
            history_text = "\n".join(history_lines)

        start_time = time.time()
        result = engine.answer(
            question=request.message,
            chat_history=history_text,
            user_id=request.user_id or "default_user",
            language=request.target_language or "en",
            level=request.complexity_level or "new"
        )
        elapsed_ms = int((time.time() - start_time) * 1000)

        return ChatResponse(
            answer=result["answer"],
            sources=[SourceInfo(**s) for s in result["sources"]],
            response_time_ms=elapsed_ms
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )


@app.get("/categories")
async def get_categories():
    """Get available legal categories."""
    return {
        "categories": [
            {"id": "fundamental_rights", "name": "Fundamental Rights", "emoji": "⚖️"},
            {"id": "criminal_law", "name": "Criminal Law (BNS/IPC)", "emoji": "🔒"},
            {"id": "family_law", "name": "Family Law", "emoji": "👨‍👩‍👧"},
            {"id": "consumer_law", "name": "Consumer Law", "emoji": "🛒"},
            {"id": "cyber_law", "name": "Cyber Law", "emoji": "💻"},
            {"id": "labour_law", "name": "Labour Law", "emoji": "👷"},
            {"id": "property_law", "name": "Property Law", "emoji": "🏠"},
            {"id": "rti", "name": "RTI (Right to Information)", "emoji": "📋"},
            {"id": "legal_aid", "name": "Free Legal Aid", "emoji": "🤝"},
        ]
    }


@app.get("/sample-questions")
async def get_sample_questions():
    """Get sample questions by category."""
    return {
        "questions": [
            "What are my rights if I'm arrested by police?",
            "How do I file an FIR if police refuses to register it?",
            "What is the punishment for domestic violence in India?",
            "How can I file a consumer complaint against Amazon for a faulty product?",
            "What is the RTI process and how do I file an RTI application?",
            "My employer is not paying minimum wages. What can I do?",
            "How do I report cybercrime/online fraud in India?",
            "What are the grounds for divorce under Hindu Marriage Act?",
            "How can I get free legal aid in India?",
            "What is POCSO Act and how does it protect children?",
            "What are the bail rights for a non-bailable offence?",
            "My landlord is trying to evict me illegally. What are my rights?",
        ]
    }


@app.post("/feedback")
async def record_feedback(req: FeedbackRequest):
    """Save user feedback (thumbs up / down) to adapt answers."""
    try:
        from memory_learning import get_learning_memory
        memory = get_learning_memory()
        memory.save_feedback(
            query=req.query,
            answer=req.answer,
            feedback=req.feedback,
            notes=req.notes or ""
        )
        return {"status": "success", "message": "Feedback recorded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/learn")
async def add_learned_insight(topic: str, insight: str):
    """Add a permanent learned insight to improve answers across users."""
    try:
        from memory_learning import get_learning_memory
        memory = get_learning_memory()
        memory.add_learned_insight(topic=topic, insight=insight)
        return {"status": "success", "message": "Insight learned"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting VakilBot Legal Assistant...")
    print("📖 Loading legal knowledge base...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
