"""Query functions that retrieve real evidence from the database.

Each function returns a dict shaped like ``EvidenceItem``
(``source_type``, ``source_name``, ``detail``) so the agent can consume
database results exactly like the previous mock data.
"""

from contextlib import contextmanager

from sqlalchemy import desc, func, or_, select

from app.db.database import SessionLocal
from app.db.models import (
    ChangeOrder,
    ProjectSchedule,
    RfiLog,
    SiteNote,
    WeatherRecord,
)

# Search terms used to find the most relevant rows for each issue type.
ISSUE_SEARCH_TERMS = {
    "weather": ["weather", "rain", "storm", "wet", "precipitation", "flood"],
    "design": ["design", "drawing", "rfi", "conflict", "clarification", "revision", "electrical"],
    "owner": ["owner", "furnished", "equipment", "delivery", "client"],
    "labor": ["labor", "crew", "shortage", "staff", "framing", "manpower"],
}


@contextmanager
def _session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def _ilike_any(column, terms):
    """Build an OR of case-insensitive LIKE clauses for the given terms."""
    return or_(*[column.ilike(f"%{term}%") for term in terms])


def _no_match(source_type: str, issue_type: str):
    return {
        "source_type": source_type,
        "source_name": "No strong match found",
        "detail": f"No matching {source_type.lower()} record found for issue type: {issue_type}.",
    }


def query_project_schedule(issue_type: str):
    terms = ISSUE_SEARCH_TERMS.get(issue_type, [])
    with _session() as session:
        stmt = select(ProjectSchedule)
        if terms:
            stmt = stmt.where(
                or_(
                    _ilike_any(ProjectSchedule.activity_name, terms),
                    _ilike_any(ProjectSchedule.responsible_party, terms),
                )
            )
        # Prefer the activity with the largest documented delay.
        stmt = stmt.order_by(desc(ProjectSchedule.delay_days)).limit(1)
        row = session.scalars(stmt).first()

    if not row:
        return _no_match("Schedule Database", issue_type)

    return {
        "source_type": "Schedule Database",
        "source_name": f"Activity {row.activity_id} - {row.activity_name}",
        "detail": (
            f"{row.activity_name} (responsible party: {row.responsible_party or 'N/A'}) "
            f"shows a {row.delay_days or 0}-day delay. Status: {row.status or 'Unknown'}."
        ),
    }


def search_site_notes(issue_type: str):
    terms = ISSUE_SEARCH_TERMS.get(issue_type, [])
    with _session() as session:
        stmt = select(SiteNote)
        if terms:
            stmt = stmt.where(
                or_(
                    _ilike_any(SiteNote.note_text, terms),
                    _ilike_any(SiteNote.category, terms),
                )
            )
        stmt = stmt.order_by(SiteNote.note_date).limit(1)
        row = session.scalars(stmt).first()

    if not row:
        return _no_match("Site Notes", issue_type)

    return {
        "source_type": "Site Notes",
        "source_name": f"{row.category or 'Daily Report'} - {row.note_date}",
        "detail": f"{row.author or 'Site staff'}: {row.note_text}",
    }


def check_weather_records(issue_type: str):
    if issue_type != "weather":
        return {
            "source_type": "Weather Records",
            "source_name": "Weather check not required",
            "detail": "The question does not appear to depend on weather evidence.",
        }

    with _session() as session:
        # Summarize the wettest day plus how many days saw measurable rain.
        peak = session.scalars(
            select(WeatherRecord)
            .order_by(desc(WeatherRecord.precipitation_inches))
            .limit(1)
        ).first()
        rainy_days = session.scalar(
            select(func.count())
            .select_from(WeatherRecord)
            .where(WeatherRecord.precipitation_inches > 0.5)
        )

    if not peak:
        return _no_match("Weather Records", issue_type)

    return {
        "source_type": "Weather Records",
        "source_name": f"Weather log near {peak.weather_date} ({peak.location})",
        "detail": (
            f"Peak precipitation of {peak.precipitation_inches} in recorded on {peak.weather_date} "
            f"({peak.condition_summary}). {rainy_days} day(s) exceeded 0.5 in of rain."
        ),
    }


def search_rfi_logs(issue_type: str):
    if issue_type != "design":
        return {
            "source_type": "RFI Log",
            "source_name": "RFI check not required",
            "detail": "The question does not appear to depend on drawing conflict or RFI evidence.",
        }

    terms = ISSUE_SEARCH_TERMS.get(issue_type, [])
    with _session() as session:
        stmt = select(RfiLog)
        if terms:
            stmt = stmt.where(
                or_(
                    _ilike_any(RfiLog.question, terms),
                    _ilike_any(RfiLog.response, terms),
                    _ilike_any(RfiLog.impact_summary, terms),
                )
            )
        stmt = stmt.order_by(RfiLog.submitted_date).limit(1)
        row = session.scalars(stmt).first()

    if not row:
        return _no_match("RFI Log", issue_type)

    return {
        "source_type": "RFI Log",
        "source_name": f"{row.rfi_id} ({row.status or 'Open'})",
        "detail": f"{row.question} Response: {row.response} Impact: {row.impact_summary}",
    }


def find_similar_change_orders(issue_type: str):
    terms = ISSUE_SEARCH_TERMS.get(issue_type, [])
    with _session() as session:
        stmt = select(ChangeOrder)
        if terms:
            stmt = stmt.where(
                or_(
                    _ilike_any(ChangeOrder.title, terms),
                    _ilike_any(ChangeOrder.reason, terms),
                    _ilike_any(ChangeOrder.summary, terms),
                )
            )
        stmt = stmt.order_by(desc(ChangeOrder.submitted_date)).limit(1)
        row = session.scalars(stmt).first()

    if not row:
        return _no_match("Change Order History", issue_type)

    return {
        "source_type": "Change Order History",
        "source_name": f"{row.co_id} - {row.title} ({row.status})",
        "detail": (
            f"Reason: {row.reason}. Requested {row.requested_days} day(s)/${row.requested_cost}. "
            f"Outcome: {row.summary}"
        ),
    }
