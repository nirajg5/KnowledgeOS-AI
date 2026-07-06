"""
Deterministic demo/mock data so the dashboard looks fully alive even
before the FastAPI backend is wired up or reachable. Every function here
mirrors the shape of the real API response documented in the backend
service layer, so swapping demo -> live data requires no UI changes.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta

random.seed(42)

FILE_TYPES = ["pdf", "docx", "txt", "csv"]
LANGUAGES = ["English", "German", "French", "Spanish", "Japanese"]
STATUSES = ["processed", "processing", "queued", "failed"]

_FILENAMES = [
    "Q3_Financial_Report", "Employee_Handbook_2026", "Vendor_Contract_Acme",
    "Product_Roadmap_v2", "Customer_Feedback_Survey", "Board_Meeting_Minutes",
    "Security_Audit_Report", "Marketing_Strategy_Deck", "Legal_NDA_Template",
    "Research_Whitepaper_AI", "Onboarding_Guide", "Sales_Pipeline_Export",
    "Compliance_Checklist", "Patent_Filing_Draft", "Annual_Sustainability_Report",
    "Customer_Support_Transcript", "Infrastructure_Runbook", "Brand_Guidelines",
    "Investor_Update_July", "API_Design_Spec",
]


def _rand_date(days_back: int = 60) -> datetime:
    return datetime.now() - timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )


def generate_documents(n: int = 20):
    docs = []
    for i in range(n):
        file_type = random.choice(FILE_TYPES)
        status = random.choices(STATUSES, weights=[0.65, 0.12, 0.13, 0.10])[0]
        pages = random.randint(1, 240) if file_type != "csv" else random.randint(1, 5000)
        docs.append({
            "id": f"doc_{i+1:04d}",
            "filename": f"{random.choice(_FILENAMES)}.{file_type}",
            "type": file_type,
            "pages": pages,
            "words": pages * random.randint(180, 420),
            "status": status,
            "language": random.choice(LANGUAGES),
            "uploaded_at": _rand_date(),
            "size_bytes": random.randint(50_000, 25_000_000),
        })
    docs.sort(key=lambda d: d["uploaded_at"], reverse=True)
    return docs


def generate_chats(n: int = 6):
    chats = []
    topics = [
        "Summarize Q3 financial report", "Key risks in vendor contract",
        "Compare roadmap v1 vs v2", "Extract action items from minutes",
        "Explain the security audit findings", "Draft exec summary of survey",
    ]
    for i in range(n):
        chats.append({
            "id": f"chat_{i+1:03d}",
            "title": topics[i % len(topics)],
            "updated_at": _rand_date(10),
            "message_count": random.randint(2, 24),
        })
    return chats


def generate_reports(n: int = 8):
    reports = []
    for i in range(n):
        reports.append({
            "id": f"rep_{i+1:04d}",
            "title": f"AI Report — {random.choice(_FILENAMES)}",
            "document": random.choice(_FILENAMES) + ".pdf",
            "created_at": _rand_date(45),
            "status": random.choices(["completed", "failed"], weights=[0.9, 0.1])[0],
        })
    return reports


def dashboard_stats(documents):
    total = len(documents)
    processed = len([d for d in documents if d["status"] == "processed"])
    total_size = sum(d["size_bytes"] for d in documents)
    return {
        "total_documents": total,
        "processed_documents": processed,
        "reports_generated": random.randint(12, 48),
        "storage_used_bytes": total_size,
    }


def document_type_distribution(documents):
    counts = {}
    for d in documents:
        counts[d["type"]] = counts.get(d["type"], 0) + 1
    return counts


def processing_status_distribution(documents):
    counts = {}
    for d in documents:
        counts[d["status"]] = counts.get(d["status"], 0) + 1
    return counts


def language_distribution(documents):
    counts = {}
    for d in documents:
        counts[d["language"]] = counts.get(d["language"], 0) + 1
    return counts


def activity_timeline(days: int = 14):
    today = datetime.now().date()
    return [
        {
            "date": today - timedelta(days=i),
            "uploads": random.randint(0, 9),
            "processed": random.randint(0, 8),
            "chats": random.randint(0, 15),
        }
        for i in range(days - 1, -1, -1)
    ]


def storage_growth(days: int = 30):
    today = datetime.now().date()
    running = random.randint(2, 6) * 1_000_000
    series = []
    for i in range(days - 1, -1, -1):
        running += random.randint(50_000, 900_000)
        series.append({"date": today - timedelta(days=i), "storage_bytes": running})
    return series


def system_status_check():
    return {
        "backend": random.choices(["online", "degraded"], weights=[0.92, 0.08])[0],
        "database": "online",
        "pageindex": random.choices(["online", "degraded"], weights=[0.9, 0.1])[0],
        "llm": "online",
    }


def ai_reply(prompt: str, doc_scope: str) -> str:
    """A canned, on-topic response used when no live LLM backend is reachable."""
    templates = [
        f"Based on **{doc_scope}**, here's what I found regarding your question:\n\n"
        f"> {prompt.strip().capitalize()}\n\n"
        "The relevant sections indicate a clear trend that supports this line of inquiry. "
        "I've cross-referenced the top matching passages below.",
        f"Great question. Looking across **{doc_scope}**, the key takeaway is that the "
        "data points to consistent patterns across the reviewed pages. Here is a concise "
        "breakdown of what stood out.",
        "I've analyzed the document context you selected. Here's a structured summary "
        "of the most relevant findings, along with supporting citations from the source text.",
    ]
    return random.choice(templates)


def citations_for(prompt: str):
    n = random.randint(1, 3)
    return [
        {
            "source": random.choice(_FILENAMES) + ".pdf",
            "page": random.randint(1, 80),
            "snippet": "…the relevant clause outlines the scope of applicability and "
                       "the conditions under which the terms remain enforceable…",
        }
        for _ in range(n)
    ]
