Requirement Document

Goal

Outcome: A verified, deterministic conversational assistant reply providing precise operational metrics and business insights derived strictly from approved DMart retail data repositories.

Stakeholder: Kavita Rao, Regional Director, who requires fast, accurate, zero-hallucination answers regarding store performance, inventory levels, and customer feedback to drive multi-store operational decisions.

Scope: Encompasses three primary datasets (store daily operations, inventory logs, and customer feedback) across five regional stores (Ahmedabad, Bengaluru, Hyderabad, Mumbai, and Pune).

Decision Boundary: The assistant may query, calculate, filter, and report approved performance metrics, summarize trends, and cross-reference store feedback. The assistant may not execute operational transactions, reorder stock, modify datasets, estimate missing data points, send outbound messages, or claim causal relationships from correlations.

Approved Field List
The assistant is strictly restricted to reporting only the following 11 approved metric fields:

From store_daily dataset: revenue_inr, daily_target_inr, footfall, stockout_hours, discount_pct, achievement_pct, performance_band.

From inventory dataset: stock_units, reorder_threshold.

From feedback dataset: rating, theme.
Note: marketing_spend_inr is deliberately excluded and not approved for reporting.
Key filter and grouping columns (store, store_id, date, product, product_id) are always permitted for filtering and aggregation, but are never returned as metrics and are excluded from the 11-field count.

Prohibited Actions

Sending outbound emails, messages, or notifications to staff or vendors.

Automatically reordering stock or triggering purchase orders.

Estimating, interpolating, or fabricating missing database records on the fly.

Stating statistical correlation as direct proof of causation.

Scope Guidance (Should Answer / Should Refuse)

Should Answer: Questions querying approved metrics across valid stores and timeframes. Example: "What was the mean daily revenue for Mumbai last week?"

Should Refuse: Questions requesting unapproved metrics, operational write actions, or external data outside the repository scope. Example: "Can you place a reorder for low inventory items in Pune?"
