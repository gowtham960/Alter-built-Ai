from app.schemas.chat import ChatResponse, EvidenceItem
from app.tools.mock_tools import (
    detect_issue_type,
    search_contract_clauses,
    query_project_schedule,
    search_site_notes,
    check_weather_records,
    search_rfi_logs,
    find_similar_change_orders,
)


def build_recommendation(issue_type: str):
    if issue_type == "weather":
        return {
            "recommendation": "Likely eligible for a schedule extension",
            "confidence": "High",
            "answer": (
                "The delay appears to be a valid change-order candidate. "
                "The contract allows extensions for abnormal weather, the schedule shows a direct delay, "
                "site notes document unsafe conditions, and weather records support the claim."
            ),
            "next_action": (
                "Draft a change-order request for a 3-day schedule extension and attach "
                "contract, schedule, site note, and weather evidence."
            ),
        }

    if issue_type == "design":
        return {
            "recommendation": "Likely eligible for a change order",
            "confidence": "High",
            "answer": (
                "The issue appears to be a valid change-order candidate because the delay was caused by "
                "a documented drawing conflict. The RFI log, schedule record, contract clause, and site notes "
                "support that work could not proceed until clarification was issued."
            ),
            "next_action": (
                "Draft a change-order request referencing RFI-014, the affected electrical rough-in activity, "
                "the site note, and the contract change-order clause."
            ),
        }

    if issue_type == "owner":
        return {
            "recommendation": "Potentially eligible for schedule and cost adjustment",
            "confidence": "Medium-High",
            "answer": (
                "The issue may qualify as an owner-caused delay. The schedule and site notes indicate that "
                "work was delayed because owner-furnished equipment arrived late. Additional delivery and cost "
                "records would strengthen the claim."
            ),
            "next_action": (
                "Collect delivery records, standby labor cost, and schedule impact evidence before submitting "
                "the change order."
            ),
        }

    if issue_type == "labor":
        return {
            "recommendation": "Likely not eligible",
            "confidence": "High",
            "answer": (
                "The claim is weak because the delay appears to be caused by contractor labor shortage. "
                "The contract treats contractor staffing problems as non-excusable delays."
            ),
            "next_action": (
                "Do not submit this as a compensable change order unless additional evidence shows the labor "
                "issue was caused by owner direction or external force majeure."
            ),
        }

    return {
        "recommendation": "Insufficient information",
        "confidence": "Low",
        "answer": (
            "The question does not clearly match a known change-order scenario. The agent needs more detail "
            "about the cause of delay, affected work activity, dates, and supporting records."
        ),
        "next_action": "Ask for delay cause, affected schedule activity, dates, and available evidence.",
    }


def analyze_change_order_question(question: str) -> ChatResponse:
    issue_type = detect_issue_type(question)

    raw_evidence = [
    search_contract_clauses(question),
    query_project_schedule(issue_type),
    search_site_notes(issue_type),
    check_weather_records(issue_type),
    search_rfi_logs(issue_type),
    find_similar_change_orders(issue_type),
]

    evidence = [EvidenceItem(**item) for item in raw_evidence]
    recommendation = build_recommendation(issue_type)

    return ChatResponse(
        recommendation=recommendation["recommendation"],
        confidence=recommendation["confidence"],
        answer=recommendation["answer"],
        evidence=evidence,
        next_action=recommendation["next_action"],
    )
