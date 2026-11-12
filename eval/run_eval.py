import os
import csv
import json
from agent.run_agent import handle, SESSION_CONTEXT

def run_evaluation():
    os.environ["WEATHER_MODE"] = "stub"
    os.environ["AGENT_LOG_PATH"] = "eval/eval_runs.jsonl"
    
    if os.path.exists("eval/eval_runs.jsonl"):
        os.remove("eval/eval_runs.jsonl")
        
    SESSION_CONTEXT.clear()
    
    with open("eval/golden_set.csv", mode="r") as f:
        reader = csv.DictReader(f)
        cases = list(reader)
        
    results = []
    
    for c in cases:
        os.environ["SIMULATE_DB_FAILURES"] = str(c["simulate_failures"])
        res = handle(c["question"], session_id=c["session_id"])
        
        actual_status = res["status"]
        intent_match = (res["intent"] == c["expected_intent"])
        
        # Check substrings
        answer_text = res["answer_text"]
        expected_subs = c["expected_contains"].split("|")
        contains_match = True
        for sub in expected_subs:
            sub = sub.strip()
            if sub not in answer_text:
                # Check numeric tolerance within 0.01 if applicable
                try:
                    sub_val = float(sub)
                    found_close = False
                    import re
                    nums = re.findall(r"\b\d+(?:\.\d+)?\b", answer_text)
                    for n in nums:
                        if abs(float(n) - sub_val) <= 0.01:
                            found_close = True
                            break
                    if not found_close:
                        contains_match = False
                        break
                except ValueError:
                    contains_match = False
                    break
                    
        passed = (actual_status == c["expected_status"]) and intent_match and contains_match
        
        results.append({
            "case_id": c["case_id"],
            "category": c["category"],
            "expected_status": c["expected_status"],
            "actual_status": actual_status,
            "intent_match": intent_match,
            "contains_match": contains_match,
            "latency_ms": res["latency_ms"],
            "tokens_est": res["tokens_est"],
            "tool_calls": res["tool_calls"],
            "ungrounded_numbers": res["ungrounded_numbers"],
            "budget_exceeded": res["budget_exceeded"],
            "passed": passed
        })
        
    with open("eval/eval_results.csv", mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
        
    print("Evaluation completed successfully. Results written to eval/eval_results.csv and log to eval/eval_runs.jsonl.")

if __name__ == "__main__":
    run_evaluation()
