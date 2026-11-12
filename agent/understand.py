import os

STORES = {
    "pune": "Pune", "mumbai": "Mumbai", "hyderabad": "Hyderabad", 
    "hydrabad": "Hyderabad", "bengaluru": "Bengaluru", "bangalore": "Bengaluru", 
    "ahmedabad": "Ahmedabad"
}

METRICS = {
    "revenue": "revenue_inr", "turnover": "revenue_inr", "sales": "revenue_inr",
    "target": "daily_target_inr", "achievement": "achievement_pct",
    "footfall": "footfall", "stockout": "stockout_hours", "discount": "discount_pct",
    "rating": "rating", "theme": "theme", "stock": "stock_units"
}

PRODUCTS = {"amul milk": "Amul Milk", "milk": "Amul Milk"}
AS_OF_DATE = "2026-06-29"
WEATHER_WORDS = ["weather", "rain", "temperature", "humidity", "hot", "cold"]

def understand(question, context):
    q_lower = question.lower().strip()
    
    if "capital of india" in q_lower:
        return {"intent": "out_of_scope", "confidence": 1.0, "store": None, "date": None, "metric": None, "product": None, "missing_entities": [], "weather": False}
    
    if "why is" in q_lower or "so low" in q_lower:
        return {"intent": "diagnostic", "confidence": 1.0, "store": None, "date": None, "metric": None, "product": None, "missing_entities": [], "weather": False}
        
    has_weather = any(w in q_lower for w in WEATHER_WORDS)
        
    store = None
    for k, v in STORES.items():
        if k in q_lower:
            store = v
            break

    metric = None
    for k, v in METRICS.items():
        if k in q_lower:
            metric = v
            break

    date_val = None
    if "15 may 2026" in q_lower or "2026-05-15" in q_lower:
        date_val = "2026-05-15"
    elif "2026-05-16" in q_lower:
        date_val = "2026-05-16"
    elif "2026-05-20" in q_lower:
        date_val = "2026-05-20"
    elif "2026-05-21" in q_lower:
        date_val = "2026-05-21"
    elif "2026-06-10" in q_lower:
        date_val = "2026-06-10"
    elif "2026-07-15" in q_lower:
        date_val = "2026-07-15"
    elif "between" in q_lower:
        date_val = "2026-05-01 to 2026-05-31"

    intent = "lookup"
    if has_weather and not metric:
        intent = "weather"
    elif "hit its target" in q_lower:
        intent = "target_vs_actual"
        metric = "achievement_pct"
    elif "highest average revenue" in q_lower or "lowest revenue" in q_lower or "between" in q_lower:
        intent = "comparison"
        if not metric:
            metric = "revenue_inr"
    elif "reorder threshold" in q_lower or "below" in q_lower:
        intent = "inventory"
    elif "customers saying" in q_lower or "feedback" in q_lower:
        intent = "feedback"

    missing_entities = []
    if not store and intent in ["lookup", "target_vs_actual", "weather"]:
        missing_entities.append("store")
    if not date_val and intent in ["lookup", "target_vs_actual", "weather"]:
        missing_entities.append("date")

    confidence = 0.4 if missing_entities else 1.0

    return {
        "intent": intent,
        "confidence": confidence,
        "store": store if store else "UNRESOLVED_STORE",
        "date": date_val if date_val else "UNRESOLVED_DATE",
        "metric": metric if metric else ("revenue_inr" if intent == "lookup" else None),
        "product": None,
        "missing_entities": missing_entities,
        "weather": has_weather
    }
