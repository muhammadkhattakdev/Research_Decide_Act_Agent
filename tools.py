from pydantic import BaseModel, Field
from typing import List
import datetime


# -------- TOOL 1: SEARCH --------

class SearchParams(BaseModel):
    query: str = Field(..., description="Search query to look up in the knowledge base")


def search_knowledge_base(query: str) -> str:
    """
    Searches a mock internal knowledge base.
    """
    knowledge_base = {
        "ai agents": "AI agents are systems that can reason, plan, and act using tools.",
        "rag": "RAG stands for Retrieval-Augmented Generation.",
        "llm": "Large Language Models generate text based on probability distributions."
    }

    for key, value in knowledge_base.items():
        if key in query.lower():
            return value

    return "No relevant information found."


# -------- TOOL 2: SUMMARIZE --------

class SummarizeParams(BaseModel):
    text: str = Field(..., description="Text to summarize")


def summarize_text(text: str) -> str:
    """
    Produces a short summary of given text.
    """
    return f"Summary: {text[:120]}..."


# -------- TOOL 3: REPORT GENERATION --------

class ReportParams(BaseModel):
    title: str = Field(..., description="Title of the report")
    summary: str = Field(..., description="Summary content")


def generate_report(title: str, summary: str) -> str:
    """
    Generates a formatted report.
    """
    date = datetime.date.today().isoformat()
    return (
        f"REPORT TITLE: {title}\n"
        f"DATE: {date}\n\n"
        f"{summary}"
    )


# -------- TOOL 4: EMAIL --------

class EmailParams(BaseModel):
    recipient: str = Field(..., description="Recipient email address")
    report: str = Field(..., description="Report content")


def send_email(recipient: str, report: str) -> str:
    """
    Mock email sender.
    """
    return f"Email successfully sent to {recipient}."


