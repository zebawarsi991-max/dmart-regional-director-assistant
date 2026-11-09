import re
from decimal import Decimal, ROUND_HALF_UP

def format_number(val, metric):
    if val is None:
        return "N/A"
    try:
        f_val = float(val)
    except ValueError:
        return str(val)
        
    if metric == "revenue_inr" or metric == "daily_target_inr":
        return f"INR {f_val:.2f}"
    elif metric in ["discount_pct", "achievement_pct"]:
        return f"{f_val:.2f}%"
    elif metric in ["rating", "footfall", "stockout_hours"]:
        return f"{f_val:.2f}"
    elif metric in ["stock_units", "reorder_threshold"]:
        return str(int(f_val))
    else:
        return f"{f_val:.2f}"

def build_answer(parsed, fetch_result):
    intent = parsed["intent"]
    store = parsed["store"]
    date_val = parsed["date"]
    metric = parsed["metric"]
    confidence = parsed["confidence"]
    missing = parsed["missing_entities"]
    
    # Status determination via precedence rules
    status = "Answered"
    answer_text = ""
    evidence = []
    grounded_values = []
    
    if parsed["intent"] in ["out_of_scope", "diagnostic"]:
        status = "Escalated"
        answer_text = "This request is out of scope or diagnostic. An analyst or escalation is required."
    elif confidence < 0.7 or missing or store == "UNRESOLVED_STORE" or date_val == "UNRESOLVED_DATE":
        status = "Clarification Needed"
        if missing or store == "UNRESOLVED_STORE" or date_val == "UNRESOLVED_DATE":
            missing_str = ", ".join(missing) if missing else "store or date"
            answer_text = f"Clarification needed: Confidence is below 0.7 or missing required entities ({missing_str}). Please clarify."
        else:
            answer_text = "Clarification needed due to low confidence or ambiguity."
    elif fetch_result["status"] == "Safe Failure":
        status = "Safe Failure"
        answer_text = fetch_result.get("message", "Safe failure encountered.")
    elif fetch_result["status"] == "Escalated":
        status = "Escalated"
        answer_text = "Query execution failed after maximum retries. Escalated."
    else:
        # Successful fetch formatting
        attempts = fetch_result.get("attempts", 1)
        if intent == "lookup" and "results" not in fetch_result:
            val = fetch_result.get("data")
            formatted_val = format_number(val, metric)
            answer_text = f"{store}'s {metric} on {date_val} was {formatted_val}."
            clean_val_str = f"{float(val):.2f}" if isinstance(val, (int, float, Decimal)) else str(val)
            grounded_values.append(clean_val_str)
            evidence.append({"source": "store_daily", "fields": [metric], "store": store, "date": date_val})
            
        elif intent == "target_vs_actual":
            rev = fetch_result.get("revenue")
            tgt = fetch_result.get("target")
            ach = fetch_result.get("achievement")
            band = fetch_result.get("band")
            
            answer_text = f"{store} on {date_val}: revenue INR {rev:.2f}, target INR {tgt:.2f}, achievement {ach:.2f}%, performance band {band}."
            grounded_values.extend([f"{rev:.2f}", f"{tgt:.2f}", f"{ach:.2f}"])
            evidence.append({"source": "store_daily", "fields": ["revenue_inr", "daily_target_inr", "achievement_pct", "performance_band"], "store": store, "date": date_val})
            
            if band == "Poor" and float(ach) < 75.0:
                status = "Drafted" # Alert fired
                
        elif intent == "comparison":
            results = fetch_result.get("results", [])
            parts = []
            for r in results:
                parts.append(f"{r['store']} {format_number(r['value'], metric)}")
                grounded_values.append(f"{r['value']:.2f}")
            answer_text = f"Comparison results for {metric}: " + "; ".join(parts) + "."
            evidence.append({"source": "store_daily", "fields": [metric], "store": "all", "date": date_val})
            
        elif intent == "inventory":
            rows = fetch_result.get("rows", [])
            if not rows:
                answer_text = f"No store is below its reorder threshold for {parsed.get('product', 'the product')}."
            else:
                parts = [f"{r['store']} {r['stock_units']} units against threshold {r['reorder_threshold']}" for r in rows]
                for r in rows:
                    grounded_values.extend([str(r['stock_units']), str(r['reorder_threshold'])])
                answer_text = "Stores below reorder threshold: " + "; ".join(parts) + "."
            evidence.append({"source": "inventory", "fields": ["stock_units", "reorder_threshold"], "store": store if store else "all", "date": None})
            
        elif intent == "feedback":
            avg_r = fetch_result.get("avg_rating")
            rated_c = fetch_result.get("rated_count")
            total_c = fetch_result.get("total_count")
            theme = fetch_result.get("theme")
            answer_text = f"Customer feedback for {store}: average rating {avg_r:.2f}, {rated_c} rated of {total_c}, most frequent theme {theme}."
            grounded_values.extend([f"{avg_r:.2f}", str(rated_c), str(total_c)])
            evidence.append({"source": "feedback", "fields": ["rating", "theme"], "store": store, "date": None})

    # Ungrounded numbers check (must be 0)
    # Count numbers in answer_text that are not in grounded_values
    number_pattern = re.compile(r"\b\d+(?:\.\d+)?\b")
    all_numbers_in_text = number_pattern.findall(answer_text)
    ungrounded_count = 0
    for num in all_numbers_in_text:
        if num not in grounded_values:
            ungrounded_count += 1

    return {
        "status": status,
        "answer_text": answer_text,
        "evidence": evidence,
        "grounded_values": grounded_values,
        "ungrounded_numbers": ungrounded_count
    }
