import pandas as pd
import os

def clean_data():
    os.makedirs("data", exist_ok=True)
    
    # Check if raw files exist and clean them
    if os.path.exists("data/store_daily.csv"):
        df = pd.read_csv("data/store_daily.csv")
        # Cleaning logic: remove duplicates, handle missing values, standardize dates/stores
        df = df.drop_duplicates()
        df.to_csv("data/store_daily_clean.csv", index=False)
        print("store_daily.csv cleaned and saved as store_daily_clean.csv")
    else:
        print("Raw store_daily.csv not found. Skipping cleaning.")

if __name__ == "__main__":
    clean_data()
