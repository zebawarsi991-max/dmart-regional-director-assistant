import re
from datetime import datetime
from difflib import SequenceMatcher

AS_OF_DATE = "2026-06-30"

VALID_STORES = ["Ahmedabad", "Bengaluru", "Hyderabad", "Mumbai", "Pune"]
STORE_ALIASES = {"bangalore": "Bengaluru"}

METRIC_MAP = {
    "revenue": "revenue_inr",
    "sales": "revenue_inr",
    "turnover": "revenue_inr",
    "earnings": "revenue_inr",
    "revenue_inr": "revenue_inr",
    "target": "daily_target_inr",
    "daily_target_inr": "daily_target_inr",
    "footfall": "footfall",
    "visitors": "footfall",
    "stockout": "stockout_hours",
    "stockout_hours": "stockout_hours",
    "discount": "discount_pct",
    "discount_pct": "discount_pct",
    "achievement_pct": "achievement_pct",
    "achievement": "achievement_pct",
    "performance_band": "performance_band",
    "performance band": "performance_band",
    "stock_units": "stock_units",
    "reorder_threshold": "reorder_threshold",
    "rating": "rating",
    "theme": "theme"
}

UNSUPPORTED_METRICS = [
    "profit", "margin", "marketing", "cost", "costs", "expense", "expenses",
    "shortfall", "efficiency", "weekend", "revenue per footfall", "revenue_per_footfall",
    "per footfall", "per visitor", "shortfall_inr", "marketing_efficiency", "weekend_flag"
]

STOP_WORDS = {
    "hello", "thanks", "thank", "kindly", "please", "display", "compare",
    "which", "what", "whats", "how", "why", "did", "and", "show", "check",
    "report", "where", "would", "could", "can", "will", "give", "tell", "list"
}

PROPER_NOUNS = {
    "dmart", "avenue", "supermarts", "kavita", "rao", "meteo", "github",
    "python", "sqlite", "postgresql", "markdown"
}

PRODUCTS = [
    "Amul Milk 1L", "Amul Milk", "Fortune Oil 1L", "Fortune Oil",
    "Iodised Salt 1kg", "Iodised Salt", "Basmati Rice 5kg", "Basmati Rice"
]

FULL_MONTHS = {
    "january": "01", "february": "02", "march": "03", "april": "04",
    "may": "05", "june": "06", "july": "07", "august": "08",
    "september": "09", "october": "10", "november": "11", "december": "12"
}

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def parse_closed_grammar_date(text):
    text_lower = text.lower()
    
    # 1. Yesterday
    if "yesterday" in text_lower:
        return "2026-06-29", 1.0, False

    # 2. ISO Date YYYY-MM-DD
    iso_match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", text)
    if iso_match:
        d_str = iso_match.group(1)
        try:
            datetime.strptime(d_str, "%Y-%m-%d")
            return d_str, 1.0, False
        except ValueError:
            return "UNRESOLVED_DATE", 0.4, True

    # 3. D Month YYYY (Full month name only)
    d_m_y = re.search(
        r"\b(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})\b",
        text_lower
    )
    if d_m_y:
        day = d_m_y.group(1).zfill(2)
        month = FULL_MONTHS[d_m_y.group(2)]
        year = d_m_y.group(3)
        d_str = f"{year}-{month}-{day}"
        try:
            datetime.strptime(d_str, "%Y-%m-%d")
            return d_str, 1.0, False
        except ValueError:
            return "UNRESOLVED_DATE", 0.4, True

    # 4. Between <date> and <date>
    between_match = re.search(
        r"\bbetween\s+(\d{4}-\d{2}-\d{2})\s+and\s+(\d{4}-\d{2}-\d{2})\b",
        text_lower
    )
    if between_match:
        d1, d2 = between_match.group(1), between_match.group(2)
        try:
            dt1 = datetime.strptime(d1, "%Y-%m-%d")
            dt2 = datetime.strptime(d2, "%Y-%m-%d")
            if dt1 <= dt2:
                return f"{d1} to {d2}", 1.0, False
            else:
                return "UNRESOLVED_DATE", 0.4, True
        except ValueError:
            return "UNRESOLVED_DATE", 0.4, True

    # Check for date-like triggers outside the closed grammar
    unresolved_triggers = [
        "last week", "next week", "this week", "this month", "last month", "next month",
        "today", "tomorrow", "q1", "q2", "q3", "q4", "2026", "ytd", "eod", "month to date",
        "15 jun 2026", "15th may 2026", "may 15, 2026", "20260515", "2026-5-15"
    ]
    if any(trg in text_lower for trg in unresolved_triggers):
        return "UNRESOLVED_DATE", 0.4, True

    for month_name in FULL_MONTHS.keys():
        if month_name in text_lower:
            # Check for verbs May / March exception
            if month_name == "may" and ("may i" in text_lower or "may we" in text_lower or "may have" in text_lower):
                continue
            return "UNRESOLVED_DATE", 0.4, True

    return None, 1.0, False


def resolve_store_and_confidence(question):
    words = re.findall(r"\b[\w']+\b", question)
    
    # Exact Match & Aliases
    for w in words:
        clean_w = re.sub(r"'s$", "", w, flags=re.IGNORECASE).capitalize()
        if clean_w in VALID_STORES:
            return clean_w, 1.0, False
        if clean_w.lower() in STORE_ALIASES:
            return STORE_ALIASES[clean_w.lower()], 1.0, False

    # Check for Persona/Brand Nouns acting as Unresolved Store
    q_lower = question.lower()
    if any(f"{noun}'s" in q_lower or f"for {noun}" in q_lower or f"in {noun}" in q_lower for noun in PROPER_NOUNS):
        return "UNRESOLVED_STORE", 0.4, True

    # Candidate Word Fuzzy Match Execution
    tokens = question.split()
    for idx, token in enumerate(tokens):
        clean_token = re.sub(r"[^\w']", "", token)
        base = re.sub(r"'s$", "", clean_token, flags=re.IGNORECASE)
        
        if len(base) >= 5 and (clean_token[0].isupper() or "'s" in clean_token.lower()):
            if idx == 0 and not "'s" in clean_token.lower():
                continue
            if base.lower() in STOP_WORDS or base.lower() in PROPER_NOUNS:
                continue

            best_score = 0.0
            best_match = None
            for s in VALID_STORES:
                score = SequenceMatcher(None, base.lower(), s.lower()).ratio()
                if score > best_score:
                    best_score = score
                    best_match = s

            if best_score >= 0.7:
                return best_match, round(best_score, 2), False
            elif best_score >= 0.5 or "'s" in clean_token.lower() or idx > 0:
                return "UNRESOLVED_STORE", 0.4, True

    return None, 1.0, False


def understand(question, context=None):
    if context is None:
        context = {}

    q_lower = question.lower()
    clean_q = q_lower.replace("_", " ")

    # Intent 1: Out of Scope / Override checks
    prohibited_imperatives = ["ignore", "disregard", "override", "bypass", "forget", "send", "email", "whatsapp", "purchase", "buy", "restock"]
    if any(p in clean_q for p in prohibited_imperatives) or "place an order" in clean_q:
        if not any(noun in clean_q for noun in ["threshold", "level", "point"]):
            return {
                "intent": "out_of_scope", "store": None, "metric": None,
                "date": None, "product": None, "weather": False,
                "confidence": 1.0, "missing_entities": []
            }

    # Intent 2: Unsupported Metric check
    if any(m in clean_q for m in UNSUPPORTED_METRICS):
        return {
            "intent": "unsupported_metric", "store": None, "metric": None,
            "date": None, "product": None, "weather": False,
            "confidence": 1.0, "missing_entities": []
        }

    # Entity Extraction
    store, s_conf, s_unresolved = resolve_store_and_confidence(question)
    date_val, d_conf, d_unresolved = parse_closed_grammar_date(question)

    product = None
    for p in PRODUCTS:
        if p.lower() in clean_q:
            product = p
            break

    metric = None
    for k, v in METRIC_MAP.items():
        if re.search(r"\b" + k + r"\b", clean_q):
            metric = v
            break

    weather_requested = "weather" in clean_q or "forecast" in clean_q

    # Intent Classification in strict order
    if "why" in clean_q or "reason" in clean_q or "trend" in clean_q:
        intent = "diagnostic"
    elif product or "inventory" in clean_q or "reorder" in clean_q:
        intent = "inventory"
    elif any(f in clean_q for f in ["feedback", "rating", "ratings", "reviews", "say", "saying"]):
        intent = "feedback"
    elif any(t in clean_q for t in ["target", "achievement", "performance band", "hit", "met", "meet", "miss", "missed", "exceed", "exceeded"]):
        intent = "target_vs_actual"
    elif any(c in clean_q for c in ["which", "highest", "lowest", "best", "worst"]) and not store:
        intent = "comparison"
    elif weather_requested and not metric:
        intent = "weather"
    elif metric or store or date_val:
        intent = "lookup"
        if context.get("last_intent") == "target_vs_actual" and not metric:
            intent = "target_vs_actual"
    else:
        intent = "out_of_scope"

    # Handle Session Context Carryover
    if not store and not s_unresolved and context.get("store") and intent not in ["comparison", "out_of_scope", "unsupported_metric", "diagnostic"]:
        store = context.get("store")

    if not date_val and not d_unresolved and context.get("date") and intent in ["lookup", "target_vs_actual", "weather", "comparison"]:
        date_val = context.get("date")

    if not metric and context.get("metric") and intent in ["lookup", "comparison"]:
        metric = context.get("metric")

    if not product and context.get("product") and intent == "inventory":
        product = context.get("product")

    # Missing Entities calculation
    missing = []
    if intent == "lookup":
        if not store or store == "UNRESOLVED_STORE": missing.append("store")
        if not metric: missing.append("metric")
        if not date_val or date_val == "UNRESOLVED_DATE": missing.append("date")
    elif intent == "target_vs_actual":
        if not store or store == "UNRESOLVED_STORE": missing.append("store")
        if not date_val or date_val == "UNRESOLVED_DATE": missing.append("date")
    elif intent == "comparison":
        if not metric: missing.append("metric")
        if not date_val or date_val == "UNRESOLVED_DATE": missing.append("date")
    elif intent == "inventory":
        if not product: missing.append("product")

    confidence = min(s_conf, d_conf)
    if missing or s_unresolved or d_unresolved:
        confidence = 0.4

    return {
        "intent": intent,
        "store": store,
        "metric": metric,
        "date": date_val,
        "product": product,
        "weather": weather_requested,
        "confidence": round(confidence, 2),
        "missing_entities": missing
    }
