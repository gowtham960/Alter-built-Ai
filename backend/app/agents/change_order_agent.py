import json
import os

from groq import Groq
from app.db.repositories import (
    check_weather_records,
    find_similar_change_orders,
    query_project_schedule,
    search_document_chunks,
    search_rfi_logs,
    search_site_notes,
)

from app.db.repositories import (
    check_weather_records,
    find_similar_change_orders,
    query_project_schedule,
    search_rfi_logs,
    search_site_notes,
)
from app.schemas.chat import ChatResponse, EvidenceItem
from app.tools.mock_tools import detect_issue_type, search_contract_clauses

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_recommendation(issue_type: str, evidence: list):
    evidence_text = "\n".join(
        f"- [{item['source_type']}] {item['source_name']}: {item['detail']}"
        for item in evidence
    )

    prompt = f"""You are a construction change-order expert.
Issue type: {issue_type}
Evidence gathered:
{evidence_text}

Based on this evidence, respond in this exact JSON format:
{{
  "recommendation": "one sentence recommendation",
  "confidence": "High / Medium / Low",
  "answer": "2-3 sentence explanation",
  "next_action": "one sentence next step"
}}
Respond with JSON only, no extra text."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return json.loads(response.choices[0].message.content)


def analyze_change_order_question(question: str) -> ChatResponse:
    issue_type = detect_issue_type(question)

    raw_evidence = [
    search_contract_clauses(question),
    query_project_schedule(issue_type),
    search_site_notes(issue_type),
    check_weather_records(issue_type),
    search_rfi_logs(issue_type),
    find_similar_change_orders(issue_type),
    search_document_chunks(question),
]

    recommendation = build_recommendation(issue_type, raw_evidence)
    evidence = [EvidenceItem(**item) for item in raw_evidence]

    return ChatResponse(
        recommendation=recommendation["recommendation"],
        confidence=recommendation["confidence"],
        answer=recommendation["answer"],
        evidence=evidence,
        next_action=recommendation["next_action"],
    )