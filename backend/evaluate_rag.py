"""
RAG Evaluation Script for Alter Built AI
Tests retrieval, relevance, generation, and end-to-end accuracy.
"""

import json
import os
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

# Test cases: question, expected issue type, expected evidence sources, expected recommendation keyword
TEST_CASES = [
    {
        "id": "TC-001",
        "category": "Weather Delay",
        "question": "Rain delayed the concrete pour for 3 days. Can we request a schedule extension?",
        "expected_issue": "weather",
        "expected_sources": ["Weather Records", "Schedule Database", "Site Notes", "Contract"],
        "expected_recommendation_keywords": ["extension", "weather", "eligible"],
        "expected_confidence": "High",
    },
    {
        "id": "TC-002",
        "category": "Design Conflict",
        "question": "The electrical rough-in was delayed because drawings had a conflict and an RFI was needed. Is this a change order?",
        "expected_issue": "design",
        "expected_sources": ["RFI Log", "Schedule Database", "Contract"],
        "expected_recommendation_keywords": ["change order", "design", "eligible"],
        "expected_confidence": "High",
    },
    {
        "id": "TC-003",
        "category": "Labor Shortage",
        "question": "Our framing crew was short-staffed for a week. Can we claim a delay?",
        "expected_issue": "labor",
        "expected_sources": ["Change Order History", "Contract"],
        "expected_recommendation_keywords": ["not eligible", "rejected", "shortage"],
        "expected_confidence": "High",
    },
    {
        "id": "TC-004",
        "category": "Owner Delay",
        "question": "The owner failed to deliver the HVAC equipment on time causing a 5-day delay. Can we claim compensation?",
        "expected_issue": "owner",
        "expected_sources": ["Schedule Database", "Contract"],
        "expected_recommendation_keywords": ["eligible", "owner", "equitable"],
        "expected_confidence": ["High", "Medium-High"],
    },
]


def evaluate_retrieval(response, expected_sources):
    """Check if expected evidence sources are present in response."""
    actual_sources = [e["source_type"] for e in response["evidence"]]
    found = [s for s in expected_sources if s in actual_sources]
    score = len(found) / len(expected_sources)
    return {
        "score": round(score, 2),
        "expected": expected_sources,
        "found": found,
        "missing": [s for s in expected_sources if s not in actual_sources],
    }


def evaluate_relevance(response):
    """Check if evidence details are non-empty and meaningful."""
    evidence = response["evidence"]
    relevant = [
        e for e in evidence
        if e["detail"] and
        "not required" not in e["detail"].lower() and
        "no matching" not in e["detail"].lower() and
        "no strong match" not in e["detail"].lower()
    ]
    score = len(relevant) / len(evidence) if evidence else 0
    return {
        "score": round(score, 2),
        "total_evidence": len(evidence),
        "relevant_evidence": len(relevant),
    }


def evaluate_generation(response, expected_keywords, expected_confidence):
    """Check if AI answer contains expected keywords and confidence."""
    answer = (response["recommendation"] + " " + response["answer"]).lower()
    found_keywords = [k for k in expected_keywords if k.lower() in answer]
    keyword_score = len(found_keywords) / len(expected_keywords)

    if isinstance(expected_confidence, list):
        confidence_match = response["confidence"] in expected_confidence
    else:
        confidence_match = response["confidence"] == expected_confidence

    return {
        "score": round(keyword_score, 2),
        "confidence_match": confidence_match,
        "actual_confidence": response["confidence"],
        "found_keywords": found_keywords,
        "missing_keywords": [k for k in expected_keywords if k.lower() not in answer],
    }


def evaluate_end_to_end(response):
    """Check if response has all required fields with meaningful content."""
    required_fields = ["recommendation", "confidence", "answer", "evidence", "next_action"]
    all_present = all(response.get(f) for f in required_fields)
    has_evidence = len(response.get("evidence", [])) > 0
    return {
        "score": 1.0 if (all_present and has_evidence) else 0.0,
        "all_fields_present": all_present,
        "has_evidence": has_evidence,
    }


def run_evaluation():
    print("\n" + "="*60)
    print("ALTER BUILT AI - RAG EVALUATION REPORT")
    print(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    results = []
    total_scores = {"retrieval": [], "relevance": [], "generation": [], "e2e": []}

    for tc in TEST_CASES:
        print(f"\n📋 {tc['id']} - {tc['category']}")
        print(f"   Question: {tc['question'][:70]}...")

        try:
            res = requests.post(
                f"{API_URL}/ask",
                json={"question": tc["question"]},
                timeout=60,
            )
            response = res.json()

            retrieval = evaluate_retrieval(response, tc["expected_sources"])
            relevance = evaluate_relevance(response)
            generation = evaluate_generation(
                response,
                tc["expected_recommendation_keywords"],
                tc["expected_confidence"],
            )
            e2e = evaluate_end_to_end(response)

            overall = round(
                (retrieval["score"] + relevance["score"] + generation["score"] + e2e["score"]) / 4, 2
            )

            print(f"   ✅ Retrieval Score:   {retrieval['score']} — Found: {retrieval['found']}")
            print(f"   ✅ Relevance Score:   {relevance['score']} — {relevance['relevant_evidence']}/{relevance['total_evidence']} evidence items relevant")
            print(f"   ✅ Generation Score:  {generation['score']} — Keywords found: {generation['found_keywords']}")
            print(f"   ✅ End-to-End Score:  {e2e['score']} — All fields present: {e2e['all_fields_present']}")
            print(f"   🎯 Overall Score:     {overall}")

            if retrieval["missing"]:
                print(f"   ⚠️  Missing sources: {retrieval['missing']}")
            if generation["missing_keywords"]:
                print(f"   ⚠️  Missing keywords: {generation['missing_keywords']}")

            total_scores["retrieval"].append(retrieval["score"])
            total_scores["relevance"].append(relevance["score"])
            total_scores["generation"].append(generation["score"])
            total_scores["e2e"].append(e2e["score"])

            results.append({"test_case": tc["id"], "overall": overall})

        except Exception as e:
            print(f"   ❌ ERROR: {e}")

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    avg_retrieval = round(sum(total_scores["retrieval"]) / len(total_scores["retrieval"]), 2)
    avg_relevance = round(sum(total_scores["relevance"]) / len(total_scores["relevance"]), 2)
    avg_generation = round(sum(total_scores["generation"]) / len(total_scores["generation"]), 2)
    avg_e2e = round(sum(total_scores["e2e"]) / len(total_scores["e2e"]), 2)
    overall_avg = round((avg_retrieval + avg_relevance + avg_generation + avg_e2e) / 4, 2)

    print(f"   Avg Retrieval Score:  {avg_retrieval}")
    print(f"   Avg Relevance Score:  {avg_relevance}")
    print(f"   Avg Generation Score: {avg_generation}")
    print(f"   Avg End-to-End Score: {avg_e2e}")
    print(f"\n   🏆 OVERALL RAG SCORE: {overall_avg} / 1.0  ({int(overall_avg*100)}%)")
    print("="*60)


if __name__ == "__main__":
    run_evaluation()