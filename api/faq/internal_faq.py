"""
InsightPulse AI - Internal FAQ Search System
Searchable knowledge base about the dataset and insurance domain.
"""
import json
from pathlib import Path
from typing import List, Dict

FAQ_PATH = Path(__file__).parent / "faq_data.json"
_faq_cache: List[Dict] = []


def _load_faq() -> List[Dict]:
    global _faq_cache
    if not _faq_cache and FAQ_PATH.exists():
        with open(FAQ_PATH, "r", encoding="utf-8") as f:
            _faq_cache = json.load(f)
    return _faq_cache


def search_faq(query: str, top_k: int = 5) -> List[Dict]:
    """Simple keyword-based FAQ search."""
    faqs = _load_faq()
    if not query.strip():
        return faqs[:top_k]
    
    query_lower = query.lower()
    scored = []
    for entry in faqs:
        score = 0
        text = (entry.get("question","") + " " + entry.get("answer","") + " " + " ".join(entry.get("tags",[]))).lower()
        for word in query_lower.split():
            if len(word) > 2 and word in text:
                score += text.count(word)
        if score > 0:
            scored.append((score, entry))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    return [e for _, e in scored[:top_k]] if scored else []


def get_all_categories() -> List[str]:
    faqs = _load_faq()
    return sorted(set(e.get("category", "General") for e in faqs))


def get_faq_by_category(category: str) -> List[Dict]:
    faqs = _load_faq()
    return [e for e in faqs if e.get("category") == category]


def get_all_faqs() -> List[Dict]:
    return _load_faq()
