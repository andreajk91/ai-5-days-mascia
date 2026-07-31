"""
Dry Run Test Script for ADK 2.0 Graph Workflow.
Tests end-to-end execution across Politics, Economics, and Science domains.
"""

import sys
sys.path.append(".")

from src.graph_workflow import BlogWriterGraphWorkflow


def run_test_suite():
    workflow = BlogWriterGraphWorkflow()
    
    test_cases = [
        {"topic": "Global Renewable Energy Agreements 2026", "domain": "Politicals"},
        {"topic": "Inflation Trends and Interest Rate Decisions", "domain": "Economics"},
        {"topic": "Breakthrough Quantum Computing Chips in Space Research", "domain": "Science"}
    ]
    
    print("==================================================")
    print("🧪 STARTING ADK 2.0 MULTI-AGENT GRAPH DRY RUN TEST")
    print("==================================================")
    
    results = []
    for test in test_cases:
        review_payload = workflow.draft_and_evaluate_article(topic=test["topic"], domain=test["domain"], journalist_id="journalist_alex")
        session_id = review_payload["session_id"]
        pub_result = workflow.publish_approved_article(session_id=session_id)
        pub_result["judge_audit"] = review_payload["judge_audit"]
        results.append(pub_result)
        
    print("\n==================================================")
    print("✅ ALL 3 DOMAIN WORKFLOW TESTS PASSED CLEANLY!")
    print("==================================================")
    for r in results:
        print(f" Article ID: {r['article_id']} | Domain: {r['domain']} | Title: '{r['article']['title']}'")
        print(f" GCS URI: {r['gcs_uri']}")
        print(f" Judge Decision: {r['judge_audit']['decision']} (Score: {r['judge_audit']['rubric_scores']['coherence_score']:.2f})")
        print("--------------------------------------------------")



if __name__ == "__main__":
    run_test_suite()
