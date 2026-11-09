import sqlite3
import pandas as pd
import os

APPROVED_METRICS = {
    "revenue_inr",
    "daily_target_inr",
    "footfall",
    "stockout_hours",
    "discount_pct",
    "achievement_pct",
    "performance_band",
    "stock_units",
    "reorder_threshold",
    "rating",
    "theme"
}

ALLOWED_FILTERS_GROUPINGS = {
    "store",
    "store_id",
    "date",
    "product",
    "product_id"
}

def get_db_connection():
    conn = sqlite3.connect("data/dmart.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")
        print("Data directory created.")
        
    required_files = ["data/store_daily_clean.csv", "data/inventory.csv", "data/feedback.csv"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"Error: Required file {file} not found in Colab environment!")
            return

    conn = get_db_connection()
    
    df_store = pd.read_csv("data/store_daily_clean.csv")
    df_inv = pd.read_csv("data/inventory.csv")
    df_feed = pd.read_csv("data/feedback.csv")
    
    df_store.to_sql("store_daily", conn, if_exists="replace", index=False)
    df_inv.to_sql("inventory", conn, if_exists="replace", index=False)
    df_feed.to_sql("feedback", conn, if_exists="replace", index=False)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully at data/dmart.db with all 3 tables!")

def validate_query_columns(columns):
    for col in columns:
        if col not in APPROVED_METRICS and col not in ALLOWED_FILTERS_GROUPINGS:
            raise ValueError(f"Security Error: Column '{col}' is not in the approved field list.")

# Function call to execute initialization
init_db()
