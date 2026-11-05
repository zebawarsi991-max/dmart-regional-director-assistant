 Data Quality Report

Overview and Basic Details

Dataset File: data/store_daily.csv

Shape: 453 rows and 9 columns

Column Data Types:

Column Name	Data Type
date	object / str
store_id	object / str
store	object / str
footfall	float64
revenue_inr	float64
daily_target_inr	int64
marketing_spend_inr	int64
stockout_hours	float64
discount_pct	float64
Null Counts: footfall has 4 missing values. All other 8 columns have 0 missing values.

Exact Duplicate Rows: 3 exact duplicate rows.

Footfall Summary Range: Minimum = -150, Maximum = 9800.

Per-Store IQR Bounds and Extreme Values
Computed after removing 3 exact duplicate rows and treating negative footfall as missing, using linear interpolation on non-missing values:

Store	Q1 (25th)	Q3 (75th)	Lower Bound	Upper Bound	Outlier or Extreme Rows
Ahmedabad	1862.00	2141.75	1582.38	2281.38	2026-05-26 (footfall: 9800)
Bengaluru	1977.00	2186.00	1563.50	2599.50	None
Hyderabad	2053.00	2356.00	1598.50	2810.50	2026-04-21 (footfall: -150; set to missing)
Mumbai	2246.00	2542.00	1802.00	2986.00	2026-04-09 (footfall: 6100)
Pune	1434.00	1689.00	1194.75	1832.75	None
Decisions

Duplicate Rows

What was done: Removed 3 exact duplicate rows, retaining only their first occurrence.

Why this choice: Exact duplicate records distort statistical summaries such as total revenue and average footfall and lead to double counting.

Raw File Status: The raw data/store_daily.csv file still contains all 453 original rows, including the 3 duplicates appended at the end.

Negative Footfall Values

What was done: Converted negative footfall of -150 on 2026-04-21 for Hyderabad to a missing value.

Why this choice: Negative footfall is physically impossible and represents a data logging error. Treating it as missing allows us to impute a realistic value during the imputation step rather than keeping an invalid figure or filling it with zero.

Raw File Status: The raw file still retains the value -150.

Extreme Values and Outliers

What was done: Capped extreme footfall values at their store respective upper IQR bound, where Ahmedabad 9800 was capped to 2281.38 and Mumbai 6100 was capped to 2986.00.

Why cap instead of delete: Deleting these rows would destroy valid revenue, stockout, and marketing spend data recorded for those days. Capping preserves the operational record while preventing extreme spikes from skewing footfall derived metrics.

Raw File Status: The raw file still retains 9800 and 6100.

Missing Values and Imputation

What was done: Filled remaining missing footfall values using each store individual median footfall.

Why median instead of mean or zero: Filling with zero would incorrectly treat operational days as zero footfall days and crash efficiency metrics. Mean is sensitive to extreme values, whereas the per-store median provides a robust central tendency tailored to each store normal operating volume.

Raw File Status: The raw file still contains the 4 blank and missing footfall fields.
