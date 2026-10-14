"""
Continuous Intelligence & Learning Engine (memory_learning.py)
Stores conversation learnings, query topics, and user feedback.
Prevents repetitive answers and dynamically enriches the vector store over time.
"""

import os
import json
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

# Support Vercel serverless environment with /tmp storage
if os.environ.get("VERCEL") or not os.access(os.path.dirname(__file__), os.W_OK):
    DATA_DIR = os.path.join("/tmp", "vakilbot_data")
else:
    DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

LEARNINGS_FILE = os.path.join(DATA_DIR, "learnings.json")
FEEDBACK_FILE = os.path.join(DATA_DIR, "feedback.json")
TOPICS_FILE = os.path.join(DATA_DIR, "topics_history.json")


def _ensure_data_files():
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        for filepath, default_val in [
            (LEARNINGS_FILE, []),
            (FEEDBACK_FILE, []),
            (TOPICS_FILE, {})
        ]:
            if not os.path.exists(filepath):
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(default_val, f, indent=2)
    except Exception as e:
        print(f"[WARN] Error initializing data files: {e}")


class FeedbackItem(BaseModel):
    query: str
    answer: str
    feedback: str  # "thumbs_up" or "thumbs_down"
    notes: Optional[str] = ""
    timestamp: float = time.time()


class LearningMemory:
    """Manages continuous memory, avoiding repetitive answers, and continuous learning."""

    def __init__(self):
        _ensure_data_files()

    def get_user_topics_context(self, user_id: str = "default_user") -> str:
        """
        Returns what topics have already been explained to this user
        to avoid regurgitating the same foundational knowledge repeatedly.
        """
        try:
            with open(TOPICS_FILE, "r", encoding="utf-8") as f:
                topics_data = json.load(f)
            user_history = topics_data.get(user_id, [])
            if not user_history:
                return "No previous topic history."
            # Extract last 10 explored topics/questions
            recent = [item.get("summary", item.get("query", "")) for item in user_history[-10:]]
            return "Already covered topics for this user:\n- " + "\n- ".join(recent)
        except Exception as e:
            return ""

    def record_topic(self, query: str, answer_summary: str, user_id: str = "default_user"):
        """Save queried topic into persistent history."""
        try:
            with open(TOPICS_FILE, "r", encoding="utf-8") as f:
                topics_data = json.load(f)
            if user_id not in topics_data:
                topics_data[user_id] = []
            topics_data[user_id].append({
                "query": query,
                "summary": answer_summary[:180],
                "timestamp": time.time()
            })
            with open(TOPICS_FILE, "w", encoding="utf-8") as f:
                json.dump(topics_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[WARN] Could not record topic: {e}")

    def save_feedback(self, query: str, answer: str, feedback: str, notes: str = ""):
        """Record user feedback (helpful or unhelpful)."""
        try:
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                feedbacks = json.load(f)
            feedbacks.append({
                "query": query,
                "answer": answer[:300],
                "feedback": feedback,
                "notes": notes,
                "timestamp": time.time()
            })
            with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
                json.dump(feedbacks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[WARN] Could not save feedback: {e}")

    def get_learned_insights(self) -> str:
        """Retrieve insights derived from previous positive feedback and clarifications."""
        try:
            with open(LEARNINGS_FILE, "r", encoding="utf-8") as f:
                learnings = json.load(f)
            if not learnings:
                return ""
            insights = [f"- On '{item.get('topic', '')}': {item.get('insight', '')}" for item in learnings[-8:]]
            return "CUMULATIVE LEARNED INSIGHTS ACROSS USERS:\n" + "\n".join(insights)
        except Exception:
            return ""

    def add_learned_insight(self, topic: str, insight: str, source: str = "user_interaction"):
        """Add a persistent learned insight to knowledge base."""
        try:
            with open(LEARNINGS_FILE, "r", encoding="utf-8") as f:
                learnings = json.load(f)
            learnings.append({
                "topic": topic,
                "insight": insight,
                "source": source,
                "timestamp": time.time()
            })
            with open(LEARNINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(learnings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[WARN] Could not save learned insight: {e}")
            return False


_memory_instance = None

def get_learning_memory() -> LearningMemory:
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = LearningMemory()
    return _memory_instance
