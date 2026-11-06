Data Context Document

Dataset 1: Store Daily Operations (store_daily.csv / store_daily_clean.csv)

Row Count: 450 rows in the cleaned dataset (store_daily_clean.csv), originating from 453 raw rows in store_daily.csv.

Date Range: 2026-04-01 to 2026-06-29 (90 days across 5 stores).

Columns and Types:

date: object / str

store_id: object / str

store: object / str

footfall: float64

revenue_inr: float64

daily_target_inr: int64

marketing_spend_inr: int64 (Note: unapproved for reporting)

stockout_hours: float64

discount_pct: float64

Data Quality Facts: Part A found 3 exact duplicate rows, 4 missing footfall values (including 1 negative footfall value of -150 for Hyderabad on 2026-04-21), and extreme outliers (Ahmedabad at 9800 footfall and Mumbai at 6100 footfall). The cleaned dataset now guarantees zero duplicate rows, zero negative footfall values, capped extreme outliers using per-store IQR bounds, and median-imputed missing footfall values.

Supported Questions: Daily store revenue, target achievement percentages, footfall trends, stockout durations, discount rates, performance banding, and revenue-per-footfall efficiencies.

Dataset 2: Inventory (inventory.csv)

Row Count: 40 rows.

Date Range: None (inventory.csv does not contain a date column).

Columns and Types:

store_id: object / str

store: object / str

product_id: object / str

product: object / str

stock_units: int64

reorder_threshold: int64

Data Quality Facts: Validated against approved entity lists with zero null or duplicate primary entity mappings.

Supported Questions: Current stock levels, stock deficits relative to reorder thresholds, and inventory distribution across products and stores.

Dataset 3: Customer Feedback (feedback.csv)

Row Count: 200 rows.

Date Range: 2026-04-01 to 2026-06-29.

Columns and Types:

feedback_id: object / str

store_id: object / str

store: object / str

date: object / str

rating: int64

theme: object / str

Data Quality Facts: Complete feedback records with verified ratings and categorized theme tags, aligned with valid store identifiers.

Supported Questions: Customer satisfaction ratings, predominant customer feedback themes, and store-wise qualitative sentiment analysis.

Relationships and Cross-Dataset Integration

Relationship Link: All three datasets are relationally linked through the store name and store_id keys, allowing the assistant to cross-reference daily operational metrics with inventory stock levels and customer feedback themes per store location.
