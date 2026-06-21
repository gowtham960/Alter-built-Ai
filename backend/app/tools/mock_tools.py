CONTRACT_CLAUSES = [
    {
        "issue_type": "weather",
        "source_type": "Contract",
        "source_name": "Riverside Contract - Clause 8.2 Weather Delay",
        "detail": "Abnormal weather may qualify for a schedule extension if written notice is submitted within 7 days.",
    },
    {
        "issue_type": "design",
        "source_type": "Contract",
        "source_name": "Riverside Contract - Clause 9.1 Change Orders",
        "detail": "Changes caused by design revisions, drawing conflicts, or owner direction may qualify for a change order.",
    },
    {
        "issue_type": "owner",
        "source_type": "Contract",
        "source_name": "Riverside Contract - Clause 12.3 Owner-Caused Delay",
        "detail": "Owner-caused delays may qualify for schedule extension and documented cost adjustment.",
    },
    {
        "issue_type": "labor",
        "source_type": "Contract",
        "source_name": "Riverside Contract - Clause 14.6 Contractor Responsibility",
        "detail": "Labor shortages caused by contractor staffing issues are not considered excusable delays.",
    },
]


PROJECT_SCHEDULE = [
    {
        "issue_type": "weather",
        "source_type": "Schedule Database",
        "source_name": "Activity A205 - Concrete Pour",
        "detail": "Concrete pour was planned for 2026-03-13 and completed on 2026-03-17, showing a 3-day delay.",
    },
    {
        "issue_type": "design",
        "source_type": "Schedule Database",
        "source_name": "Activity A310 - Electrical Rough-In",
        "detail": "Electrical rough-in was delayed by 2 days after drawing conflict RFI-014 required clarification.",
    },
    {
        "issue_type": "owner",
        "source_type": "Schedule Database",
        "source_name": "Activity A420 - HVAC Equipment Installation",
        "detail": "HVAC installation was delayed because owner-furnished equipment arrived 5 days after the planned delivery date.",
    },
    {
        "issue_type": "labor",
        "source_type": "Schedule Database",
        "source_name": "Activity A510 - Interior Framing",
        "detail": "Interior framing was delayed by 2 days, but schedule notes identify crew shortage as the cause.",
    },
]


SITE_NOTES = [
    {
        "issue_type": "weather",
        "source_type": "Site Notes",
        "source_name": "Daily Reports March 12-14",
        "detail": "Daily reports mention heavy rain, standing water, and unsafe concrete pour conditions.",
    },
    {
        "issue_type": "design",
        "source_type": "Site Notes",
        "source_name": "Daily Report March 18",
        "detail": "Superintendent noted that electrical rough-in could not proceed because drawings S2.1 and E4.2 conflicted.",
    },
    {
        "issue_type": "owner",
        "source_type": "Site Notes",
        "source_name": "Daily Report April 4",
        "detail": "Site note says HVAC crew was ready, but owner-furnished equipment had not arrived.",
    },
    {
        "issue_type": "labor",
        "source_type": "Site Notes",
        "source_name": "Daily Report April 9",
        "detail": "Daily report says subcontractor crew was short-staffed and could not complete planned framing work.",
    },
]


WEATHER_RECORDS = [
    {
        "issue_type": "weather",
        "source_type": "Weather Records",
        "source_name": "Mock Weather Table - March 12-14",
        "detail": "Recorded precipitation exceeded 0.9 inches for three consecutive days during the planned concrete pour window.",
    }
]


RFI_LOGS = [
    {
        "issue_type": "design",
        "source_type": "RFI Log",
        "source_name": "RFI-014 Foundation and Electrical Conflict",
        "detail": "RFI-014 documents a conflict between structural and electrical drawings. Response instructed contractor to follow revised detail.",
    }
]


CHANGE_ORDER_HISTORY = [
    {
        "issue_type": "weather",
        "source_type": "Change Order History",
        "source_name": "CO-001 Weather Delay",
        "detail": "A previous weather-related delay was approved for a 2-day schedule extension when weather records and site notes supported the claim.",
    },
    {
        "issue_type": "design",
        "source_type": "Change Order History",
        "source_name": "CO-006 Drawing Conflict",
        "detail": "A previous design-conflict change order was approved after the RFI log showed a drawing discrepancy.",
    },
    {
        "issue_type": "owner",
        "source_type": "Change Order History",
        "source_name": "CO-009 Owner-Furnished Equipment Delay",
        "detail": "A prior owner-caused equipment delay was approved for 4 schedule days and documented standby cost.",
    },
    {
        "issue_type": "labor",
        "source_type": "Change Order History",
        "source_name": "CO-003 Labor Shortage Delay",
        "detail": "A previous labor-shortage claim was rejected because contractor staffing problems were not excusable under the contract.",
    },
]


def detect_issue_type(question: str) -> str:
    question_lower = question.lower()

    weather_keywords = ["rain", "weather", "storm", "precipitation", "flood", "wet"]
    design_keywords = ["drawing", "design", "rfi", "conflict", "clarification", "revision"]
    owner_keywords = ["owner", "late delivery", "equipment", "furnished", "client"]
    labor_keywords = ["labor", "crew", "shortage", "staff", "worker", "manpower"]

    if any(keyword in question_lower for keyword in weather_keywords):
        return "weather"

    if any(keyword in question_lower for keyword in design_keywords):
        return "design"

    if any(keyword in question_lower for keyword in owner_keywords):
        return "owner"

    if any(keyword in question_lower for keyword in labor_keywords):
        return "labor"

    return "general"


def _find_by_issue_type(records, issue_type: str):
    for record in records:
        if record.get("issue_type") == issue_type:
            return {
                "source_type": record["source_type"],
                "source_name": record["source_name"],
                "detail": record["detail"],
            }

    return {
        "source_type": "Source Search",
        "source_name": "No strong match found",
        "detail": f"No matching record found for issue type: {issue_type}.",
    }


def search_contract_clauses(question: str):
    issue_type = detect_issue_type(question)
    return _find_by_issue_type(CONTRACT_CLAUSES, issue_type)


def query_project_schedule(question: str):
    issue_type = detect_issue_type(question)
    return _find_by_issue_type(PROJECT_SCHEDULE, issue_type)


def query_schedule(question: str):
    return query_project_schedule(question)


def search_site_notes(question: str):
    issue_type = detect_issue_type(question)
    return _find_by_issue_type(SITE_NOTES, issue_type)


def check_weather_records(question: str):
    issue_type = detect_issue_type(question)

    if issue_type != "weather":
        return {
            "source_type": "Weather Records",
            "source_name": "Weather check not required",
            "detail": "The question does not appear to depend on weather evidence.",
        }

    return _find_by_issue_type(WEATHER_RECORDS, issue_type)


def search_rfi_logs(question: str):
    issue_type = detect_issue_type(question)

    if issue_type != "design":
        return {
            "source_type": "RFI Log",
            "source_name": "RFI check not required",
            "detail": "The question does not appear to depend on drawing conflict or RFI evidence.",
        }

    return _find_by_issue_type(RFI_LOGS, issue_type)


def find_similar_change_orders(question: str):
    issue_type = detect_issue_type(question)
    return _find_by_issue_type(CHANGE_ORDER_HISTORY, issue_type)