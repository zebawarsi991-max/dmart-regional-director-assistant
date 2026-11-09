import os
import time
import json
import uuid
from datetime import datetime
from agent.understand import understand
from agent.fetch import fetch_data
from agent.answer import build_answer

SESSION_CONTEXT = {}

def handle(question, session_id, user_id="u1"):
    start_time = time.monotonic()
    
    # Get session context
    if session_id not in SESSION_CONTEXT:
        SESSION_CONTEXT[session_id] = {}
    context = SESSION_CONTEXT[session_id]
    
    # 1. Understand
    parsed = understand(question, context)
    
    # Update context with resolved entities
    if parsed["store"] and parsed["store"] != "UNRESOLVED_STORE":
        context["store"] = parsed["store"]
    if parsed["date"] and parsed["date"] != "UNRESOLVED_DATE":
        context["date"] = parsed["date"]
    if parsed["metric"]:
        context["metric"] = parsed["metric"]
    if parsed["product"]:
        context["product"] = parsed["product"]
    context["last_intent"] = parsed["intent"]
    
    # 2. Fetch
    executed_query_info = None
    route = "none"
    tool_calls = 0
    attempts = 0
    
    if parsed["intent"] in ["lookup", "target_vs_actual", "comparison", "inventory", "feedback"] and parsed["confidence"] >= 0.7 and not parsed["missing_entities"]:
        if parsed["intent"] in ["comparison", "inventory", "feedback"] or (parsed["intent"] == "lookup" and parsed["date"] and " to " in parsed["date"]):
            route = "sql"
            tool_calls = 1
        else:
            route = "python"
            tool_calls = 1
            
        fetch_result = fetch_data(parsed)
        attempts = fetch_result.get("attempts", 1)
    else:
        fetch_result = {"status": "Safe Failure", "message": "Pre-query validation or clarification needed.", "attempts": 0}
        
    # 3. Answer / Ground / Synthesize
    answer_res = build_answer(parsed, fetch_result)
    
    end_time = time.monotonic()
    latency_ms = round((end_time - start_time) * 1000, 2)
    
    # Token estimation (whitespace-separated words in question + answer)
    tokens_est = len(question.split()) + len(answer_res["answer_text"].split())
    budget_exceeded = tokens_est > 150
    
    log_record = {
        "run_id": str(uuid.uuid4()),
        "user_id": user_id,
        "session_id": session_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "question": question,
        "intent": parsed["intent"],
        "confidence": parsed["confidence"],
        "route": route,
        "executed": executed_query_info,
        "attempts": attempts,
        "tools_called": ["weather_tool"] if parsed["weather"] else [],
        "status": answer_res["status"],
        "answer_text": answer_res["answer_text"],
        "evidence": answer_res["evidence"],
        "grounded_values": answer_res["grounded_values"],
        "latency_ms": latency_ms,
        "tokens_est": tokens_est,
        "tool_calls": tool_calls + (1 if parsed["weather"] else 0),
        "ungrounded_numbers": answer_res["ungrounded_numbers"],
        "budget_exceeded": budget_exceeded
    }
    
    log_path = os.getenv("AGENT_LOG_PATH", "logs/runs.jsonl")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(log_record) + "\n")
        
    return log_record
