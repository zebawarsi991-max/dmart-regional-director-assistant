import re

def build_answer(parsed, fetch_result, weather_result=None):
    intent = parsed["intent"]
    store = parsed["store"]
    date_val = parsed["date"]
    metric = parsed["metric"]
    
    status = "Answered"
    answer_text = ""
    evidence = []
    grounded_values = []
    
    if parsed["missing_entities"] or parsed["confidence"] < 0.7:
        return {
            "status": "Clarification Needed",
            "answer_text": "Clarification needed due to missing entities or low confidence.",
            "evidence": [], "grounded_values": [], "ungrounded_numbers": 0
        }
        
    if fetch_result.get("status") == "Safe Failure":
        return {
            "status": "Safe Failure",
            "answer_text": fetch_result.get("message", "Safe failure."),
            "evidence": [], "grounded_values": [], "ungrounded_numbers": 0
        }

    if intent == "lookup":
        val = fetch_result.get("data")
        answer_text = f"{store}'s {metric} on {date_val} was INR {float(val):.2f}."
        grounded_values.append(f"{float(val):.2f}")
        evidence.append({"source": "store_daily", "fields": [metric], "store": store, "date": date_val})
    elif intent == "weather":
        answer_text = f"Weather for {store} on {date_val}:"
    elif intent == "target_vs_actual":
        rev = fetch_result.get("revenue")
        ach = fetch_result.get("achievement")
        answer_text = f"Revenue INR {rev:.2f}, achievement {ach:.2f}%."
        grounded_values.extend([f"{rev:.2f}", f"{ach:.2f}"])
        evidence.append({"source": "store_daily", "fields": ["revenue_inr", "achievement_pct"], "store": store, "date": date_val})

    if weather_result and weather_result.get("ok"):
        t = weather_result["temperature_c"]
        h = weather_result["humidity_pct"]
        w = weather_result["wind_kmh"]
        r = weather_result["rain_mm"]
        weather_str = f" Temperature {t:.1f}C, humidity {h:.1f}%, wind {w:.1f} km/h, rain {r:.1f} mm."
        answer_text += weather_str
        grounded_values.extend([f"{t:.1f}", f"{h:.1f}", f"{w:.1f}", f"{r:.1f}"])
        evidence.append({"source": "weather_tool", "fields": ["temperature_c", "humidity_pct", "wind_kmh", "precipitation_sum"], "store": store, "date": date_val})

    number_pattern = re.compile(r"\b\d+(?:\.\d+)?\b")
    all_nums = number_pattern.findall(answer_text)
    ungrounded = sum(1 for n in all_nums if n not in grounded_values)

    return {
        "status": status,
        "answer_text": answer_text,
        "evidence": evidence,
        "grounded_values": grounded_values,
        "ungrounded_numbers": ungrounded
    }
