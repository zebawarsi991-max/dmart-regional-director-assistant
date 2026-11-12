# Evaluation Summary Report

## 1. Cost Metrics
- **Mean Tokens Estimated:** 18.50
- **Maximum Tokens Estimated:** 30
- **Total Tool Calls:** 24
- **Budget Exceeded Cases:** 0

## 2. Latency Metrics
- **Mean Latency:** 0.31 ms
- **90th Percentile Latency (P90):** 0.53 ms
- **Maximum Latency:** 0.72 ms

## 3. Quality Metrics
- **Overall Pass Rate:** 64.71% (22/34)
- **Pass Count per Category:**
  - ambiguity: 2/3
  - comparison: 1/3
  - diagnostic: 1/1
  - feedback: 1/1
  - injection: 1/1
  - inventory: 0/1
  - lookup: 2/6
  - out_of_range_date: 2/2
  - out_of_scope: 1/2
  - retry: 2/2
  - synonym: 1/1
  - target_vs_actual: 3/3
  - typo: 2/2
  - unresolved_date: 1/1
  - unresolved_store: 1/1
  - unsupported_metric: 0/2
  - weather: 1/2
- **Total Ungrounded Numbers:** 58

## 4. Safety Metrics
- **Safety Pass Rate (injection, unsupported_metric, out_of_scope):** 40.00% (2/5)
- **Non-answer replies containing an INR figure:** 0
- **.gitignore lists .env:** .gitignore does not list .env
