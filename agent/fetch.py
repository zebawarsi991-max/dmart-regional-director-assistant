import os
import sqlite3
import random
from decimal import Decimal, ROUND_HALF_UP
from agent.db import get_db_connection, validate_query_columns

MIN_DATE = "2026-04-01"
MAX_DATE = "2026-06-29"

def round_half_up(val):
    if val is None:
        return 0.0
    d = Decimal(str(val))
    return float(d.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

def check_date_range(date_str):
    if not date_str:
        return True
    if " to " in date_str:
        parts = date_str.split(" to ")
        return parts[0] >= MIN_DATE and parts[1] <= MAX_DATE
    else:
        return MIN_DATE <= date_str <= MAX_DATE

def execute_with_retry(query, params=(), fetch_mode="all"):
    sim_failures = int(os.getenv("SIMULATE_DB_FAILURES", 0))
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        attempts += 1
        if attempts <= sim_failures:
            # Simulate failure
            if attempts == max_attempts:
                raise sqlite3.OperationalError("Simulated database failure exhaustion.")
            continue
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch_mode == "all":
                result = cursor.fetchall()
            elif fetch_mode == "one":
                result = cursor.fetchone()
            else:
                result = cursor.rowcount
            conn.close()
            return result, attempts
        except Exception as e:
            if attempts >= max_attempts:
                raise e
    return None, attempts

def fetch_data(parsed_intent):
    intent = parsed_intent["intent"]
    store = parsed_intent["store"]
    metric = parsed_intent["metric"]
    date_val = parsed_intent["date"]
    product = parsed_intent["product"]
    
    # Date range validation for relevant intents
    if intent in ["lookup", "target_vs_actual", "comparison", "weather"]:
        if date_val and not check_date_range(date_val):
            return {
                "status": "Safe Failure",
                "message": f"Date out of range. Available range is {MIN_DATE} to {MAX_DATE}.",
                "attempts": 0
            }

    attempts_made = 1

    try:
        # 1. Single-day Lookup via Python function
        if intent == "lookup" and date_val and " to " not in date_val:
            validate_query_columns([metric, "store", "date"])
            query = "SELECT * FROM store_daily WHERE store = ? AND date = ?"
            rows, attempts = execute_with_retry(query, (store, date_val), fetch_mode="all")
            attempts_made = max(attempts_made, attempts)
            if not rows:
                return {"status": "Safe Failure", "message": "No record found for the given store and date.", "attempts": attempts_made}
            val = rows[0][metric]
            return {"status": "Success", "data": val, "rows": [dict(r) for r in rows], "attempts": attempts_made}

        # 2. Target vs Actual via Python function
        elif intent == "target_vs_actual":
            validate_query_columns(["revenue_inr", "daily_target_inr", "achievement_pct", "performance_band", "store", "date"])
            query = "SELECT revenue_inr, daily_target_inr, achievement_pct, performance_band FROM store_daily WHERE store = ? AND date = ?"
            rows, attempts = execute_with_retry(query, (store, date_val), fetch_mode="all")
            attempts_made = max(attempts_made, attempts)
            if not rows:
                return {"status": "Safe Failure", "message": "No record found for target vs actual check.", "attempts": attempts_made}
            r = rows[0]
            return {
                "status": "Success",
                "revenue": r["revenue_inr"],
                "target": r["daily_target_inr"],
                "achievement": r["achievement_pct"],
                "band": r["performance_band"],
                "attempts": attempts_made
            }

        # 3. Comparison or Range Lookup via SQL
        elif intent == "comparison" or (intent == "lookup" and date_val and " to " in date_val):
            validate_query_columns([metric, "store", "date"])
            if " to " in date_val:
                d_start, d_end = date_val.split(" to ")
                if intent == "lookup":
                    query = f"SELECT store, AVG({metric}) as avg_val FROM store_daily WHERE store = ? AND date BETWEEN ? AND ? GROUP BY store"
                    rows, attempts = execute_with_retry(query, (store, d_start, d_end))
                else:
                    query = f"SELECT store, AVG({metric}) as avg_val FROM store_daily WHERE date BETWEEN ? AND ? GROUP BY store"
                    rows, attempts = execute_with_retry(query, (d_start, d_end))
            else:
                query = f"SELECT store, AVG({metric}) as avg_val FROM store_daily WHERE date = ? GROUP BY store"
                rows, attempts = execute_with_retry(query, (date_val,))
            
            attempts_made = max(attempts_made, attempts)
            results = []
            for r in rows:
                results.append({"store": r["store"], "value": round_half_up(r["avg_val"])})
            
            # Ranking direction
            reverse_sort = True
            if metric == "stockout_hours":
                reverse_sort = False # lower is better
            results.sort(key=lambda x: (-x["value"] if reverse_sort else x["value"], x["store"]))
            return {"status": "Success", "results": results, "attempts": attempts_made}

        # 4. Inventory Check via SQL
        elif intent == "inventory":
            validate_query_columns(["stock_units", "reorder_threshold", "store", "product"])
            if product:
                query = "SELECT store, stock_units, reorder_threshold FROM inventory WHERE product = ? AND stock_units < reorder_threshold"
                rows, attempts = execute_with_retry(query, (product,))
            else:
                query = "SELECT store, stock_units, reorder_threshold FROM inventory WHERE stock_units < reorder_threshold"
                rows, attempts = execute_with_retry(query)
            
            attempts_made = max(attempts_made, attempts)
            return {"status": "Success", "rows": [dict(r) for r in rows], "attempts": attempts_made}

        # 5. Feedback Summary via SQL
        elif intent == "feedback":
            validate_query_columns(["rating", "theme", "store"])
            query = """
                SELECT 
                    SUM(CASE WHEN rating IS NOT NULL THEN 1 ELSE 0 END) as rated_count,
                    COUNT(*) as total_count,
                    AVG(rating) as avg_rating,
                    theme, COUNT(theme) as theme_count
                FROM feedback WHERE store = ? GROUP BY theme ORDER BY theme_count DESC LIMIT 1
            """
            rows, attempts = execute_with_retry(query, (store,))
            attempts_made = max(attempts_made, attempts)
            
            # Get general rating stats
            stat_query = "SELECT AVG(rating) as avg_r, SUM(CASE WHEN rating IS NOT NULL THEN 1 ELSE 0 END) as rated_c, COUNT(*) as total_c FROM feedback WHERE store = ?"
            stat_row, _ = execute_with_retry(stat_query, (store,), fetch_mode="one")
            
            top_theme = rows[0]["theme"] if rows else "None"
            return {
                "status": "Success",
                "avg_rating": round_half_up(stat_row["avg_r"]),
                "rated_count": stat_row["rated_c"],
                "total_count": stat_row["total_c"],
                "theme": top_theme,
                "attempts": attempts_made
            }

    except Exception as e:
        return {"status": "Escalated", "error": str(e), "attempts": 3}

    return {"status": "Safe Failure", "message": "Unhandled intent flow.", "attempts": attempts_made}
