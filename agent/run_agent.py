import os
import time
import json
import uuid
from datetime import datetime
from agent.understand import understand
from agent.fetch import fetch_data
from agent.answer import build_answer
from tools.weather import get_weather

SESSION_CONTEXT = {}

def handle(question, session_id, user_id="u1"):
    start_time = time.monotonic()
    
    if session_id not in SESSION_CONTEXT:
        SESSION_CONTEXT[session_id] = {}
    context = SESSION_CONTEXT[session_id]
    
    parsed = understand(question, context)
    
    if parsed["store"] and parsed["store"] != "UNRESOLVED_STORE":
        context["store"] = parsed["store"]
    if parsed["date"] and parsed["date"] != "UNRESOLVED_DATE":
        context["date"] = parsed["date"]
    
    route = "none"
    tool_calls = 0
    attempts = 0
    tools_called = []
    fetch_result = {}
    weather_result = None
    
    if parsed["confidence"] >= 0.7 and not parsed["missing_entities"]:
        if parsed["intent"] in ["comparison", "inventory", "feedback"]:
            route = "sql"
            tool_calls = 1
            fetch_result = fetch_data(parsed)
            attempts = fetch_result.get("attempts", 1)
        elif parsed["intent"] in ["lookup", "target_vs_actual"]:
            if parsed["weather"] and parsed["date"] and " to " not in parsed["date"]:
                route = "python+weather"
                tool_calls = 2
                tools_called = ["weather_tool"]
                weather_result = get_weather(parsed["store"], parsed["date"])
            else:
                route = "python"
                tool_calls = 1
            fetch_result = fetch_data(parsed)
            attempts = fetch_result.get("attempts", 1)
        elif parsed["intent"] == "weather":
            if parsed["date"] and " to " not in parsed["date"]:
                route = "weather"
                tool_calls = 1
                tools_called = ["weather_tool"]
                weather_result = get_weather(parsed["store"], parsed["date"])
                fetch_result = {"status": "Success"}
            else:
                fetch_result = {"status": "Safe Failure", "message": "Weather intent requires a single valid date."}
    else:
        fetch_result = {"status": "Safe Failure", "message": "Clarification needed."}
        
    answer_res = build_answer(parsed, fetch_result, weather_result)
    
    end_time = time.monotonic()
    latency_ms = round((end_time - start_time) * 1000, 2)
    tokens_est = len(question.split()) + len(answer_res["answer_text"].split())
    
    log_record = {
        "run_id": str(uuid.uuid4()),
        "user_id": user_id,
        "session_id": session_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "question": question,
        "intent": parsed["intent"],
        "confidence": parsed["confidence"],
        "route": route,
        "executed": None,
        "attempts": attempts,
        "tools_called": tools_called,
        "status": answer_res["status"],
        "answer_text": answer_res["answer_text"],
        "evidence": answer_res["evidence"],
        "grounded_values": answer_res["grounded_values"],
        "latency_ms": latency_ms,
        "tokens_est": tokens_est,
        "tool_calls": tool_calls,
        "ungrounded_numbers": answer_res["ungrounded_numbers"],
        "budget_exceeded": tokens_est > 150
    }
    
    log_path = os.getenv("AGENT_LOG_PATH", "logs/runs.jsonl")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(log_record) + "\n")
        
    return log_record
