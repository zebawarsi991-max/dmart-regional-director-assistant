import pandas as pd
import numpy as np

# Load clean and raw datasets
df_clean = pd.read_csv("data/store_daily_clean.csv")
df_raw = pd.read_csv("data/store_daily.csv")

# Prepare raw deduplicated data with negatives and extremes intact (non-missing footfall only)
df_raw_dedup = df_raw.drop_duplicates(keep="first").copy()
df_raw_valid = df_raw_dedup[df_raw_dedup["footfall"].notna()].copy()

print("--- PART A: ANALYSIS & METRICS ---")

# 1. Store Metrics Table Calculation
store_metrics = []
for store, group in df_clean.groupby("store"):
    mean_rev = group["revenue_inr"].mean()
    mean_ff = group["footfall"].mean()
    mean_so = group["stockout_hours"].mean()
    rev_per_ff = group["revenue_inr"].sum() / group["footfall"].sum()
    mean_ach = group["achievement_pct"].mean()
    poor_days = (group["performance_band"] == "Poor").sum()
    
    store_metrics.append({
        "Store": store,
        "Mean Daily Revenue": round(mean_rev, 2),
        "Mean Footfall": round(mean_ff, 2),
        "Mean Stockout Hours": round(mean_so, 2),
        "Revenue per Footfall": round(rev_per_ff, 2),
        "Mean Achievement Pct": round(mean_ach, 2),
        "Poor Band Days": poor_days
    })

# All stores pooled row
all_mean_rev = df_clean["revenue_inr"].mean()
all_mean_ff = df_clean["footfall"].mean()
all_mean_so = df_clean["stockout_hours"].mean()
all_rev_per_ff = df_clean["revenue_inr"].sum() / df_clean["footfall"].sum()
all_mean_ach = df_clean["achievement_pct"].mean()
all_poor_days = (df_clean["performance_band"] == "Poor").sum()

store_metrics.append({
    "Store": "All stores",
    "Mean Daily Revenue": round(all_mean_rev, 2),
    "Mean Footfall": round(all_mean_ff, 2),
    "Mean Stockout Hours": round(all_mean_so, 2),
    "Revenue per Footfall": round(all_rev_per_ff, 2),
    "Mean Achievement Pct": round(all_mean_ach, 2),
    "Poor Band Days": all_poor_days
})

metrics_df = pd.DataFrame(store_metrics)
print(metrics_df.to_string(index=False))

print("\n--- STOCKOUT HOURS RANKING ---")
stockout_ranking = df_clean.groupby("store")["stockout_hours"].mean().sort_values(ascending=False)
print(stockout_ranking)

print("\n--- PEARSON CORRELATIONS ---")
corr_rev_stock_all = np.corrcoef(df_clean["revenue_inr"], df_clean["stockout_hours"])[0, 1]
corr_rev_ff_all = np.corrcoef(df_clean["revenue_inr"], df_clean["footfall"])[0, 1]

pune_df = df_clean[df_clean["store"] == "Pune"]
corr_rev_stock_pune = np.corrcoef(pune_df["revenue_inr"], pune_df["stockout_hours"])[0, 1]
corr_rev_ff_pune = np.corrcoef(pune_df["revenue_inr"], pune_df["footfall"])[0, 1]

corr_rev_ff_raw = np.corrcoef(df_raw_valid["revenue_inr"], df_raw_valid["footfall"])[0, 1]

print(f"Revenue vs Stockout Hours (All 450 rows): {corr_rev_stock_all:.4f}")
print(f"Revenue vs Footfall (All 450 rows): {corr_rev_ff_all:.4f}")
print(f"Revenue vs Stockout Hours (Pune only): {corr_rev_stock_pune:.4f}")
print(f"Revenue vs Footfall (Pune only): {corr_rev_ff_pune:.4f}")
print(f"Revenue vs Footfall (Raw deduplicated with outliers/negatives): {corr_rev_ff_raw:.4f}")
