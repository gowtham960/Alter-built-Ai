def search_contract_clauses(question: str):
    return {
        "source_type": "Contract",
        "source_name": "Riverside Office Renovation Contract - Clause 8.2",
        "detail": "Weather delays caused by abnormal precipitation may qualify for schedule extension if notice is submitted within 7 days.",
    }


def query_project_schedule(question: str):
    return {
        "source_type": "Schedule Database",
        "source_name": "Activity A205 - Concrete Pour",
        "detail": "Concrete pour was planned for 2026-03-13 and completed on 2026-03-17, showing a 3-day delay.",
    }


def search_site_notes(question: str):
    return {
        "source_type": "Site Notes",
        "source_name": "Daily Reports March 12-14",
        "detail": "Daily reports mention heavy rain, standing water, and unsafe concrete pour conditions.",
    }


def check_weather_records(question: str):
    return {
        "source_type": "Weather Records",
        "source_name": "Mock Weather Table",
        "detail": "Recorded precipitation exceeded 0.9 inches for three consecutive days during the planned concrete pour window.",
    }


def find_similar_change_orders(question: str):
    return {
        "source_type": "Change Order History",
        "source_name": "CO-001 Weather Delay",
        "detail": "A previous weather-related delay was approved for a 2-day schedule extension.",
    }
