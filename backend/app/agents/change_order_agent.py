from app.schemas.chat import ChatResponse, EvidenceItem
from app.tools.mock_tools import (
    search_contract_clauses,
    query_project_schedule,
    search_site_notes,
    check_weather_records,
    find_similar_change_orders,
)


def analyze_change_order_question(question: str) -> ChatResponse:
    """Mock agent flow for the first MVP.

    Later, this will become a real agent that chooses tools dynamically,
    retrieves data from Supabase/vector search, and asks an LLM to reason
    over the evidence.
    """
    raw_evidence = [
        search_contract_clauses(question),
        query_project_schedule(question),
        search_site_notes(question),
        check_weather_records(question),
        find_similar_change_orders(question),
    ]

    evidence = [EvidenceItem(**item) for item in raw_evidence]

    return ChatResponse(
        recommendation="Likely eligible for a schedule extension",
        confidence="High",
        answer=(
            "The delay appears to be a valid change-order candidate. The contract allows "
            "extensions for abnormal weather when notice is submitted within the required "
            "window. The schedule, site notes, weather records, and prior change-order "
            "history all support the claim."
        ),
        evidence=evidence,
        next_action="Draft a change-order request for a 3-day schedule extension and attach the supporting evidence.",
    )
