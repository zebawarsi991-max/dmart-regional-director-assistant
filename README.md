# dmart-regional-director-assistant
# DMart Store Operations & Weather Analytics Assistant

## 1. Purpose
This repository implements a grounded retail analytics assistant for DMart store operations across five cities (Mumbai, Pune, Hyderabad, Bengaluru, and Ahmedabad). It answers natural-language queries regarding store revenue, daily targets, cross-store comparisons, product reorder inventory, customer feedback, and historical weather conditions while strictly preventing hallucinated numbers and ungrounded responses.

---

## 2. Setup and Execution Order
Run the following scripts in sequence from the repository root directory:

1. **Environment Setup:** Ensure Python 3.9+ is installed along with required packages (`pandas`, `numpy`, `requests`).
2. **Initialize Data & Verify Database:** Ensure the local SQLite database (`data/dmart.db`) is populated.
3. **Run Acceptance Test Suite:** Executes the 20 core acceptance test cases (`python scripts/run_acceptance.py`).
4. **Run Weather Tool Unit Tests:** Verifies stub calculations (`python -c "import tools.weather"`).
5. **Run Golden Evaluation Harness:** Evaluates the golden dataset (`python eval/run_eval.py`).
6. **Generate Evaluation Summary & Release Gate:** Computes metrics and release decisions.

---

## 3. Free Offline Execution Path
- **Local Database:** Queries execute against local SQLite (`data/dmart.db`).
- **Stub Weather Mode:** Runs deterministically using city-length and day-of-year formulas. (Weather data by Open-Meteo.com https://open-meteo.com/).
- **Offline Understanding:** Entity extraction and routing run locally without external LLM dependencies.

---

## 4. Repository Layout
- `agent/`: Core agent logic (understand, fetch, answer, run_agent)
- `data/`: Local SQLite database
- `docs/`: Release gate evaluation report
- `eval/`: Evaluation harness, golden set, and summary metrics
- `tools/`: Weather tool integration
- `scripts/`: Acceptance test runner
- `tests/`: Unit test records

---

## 5. Rounding Method
All monetary averages and percentage calculations use standard half-up rounding (`ROUND_HALF_UP`) to two decimal places via Python's `Decimal` module.

---

## 6. Known Limitations
1. Closed date and store grammar require exact formats.
2. Single-turn context scope within sessions.
3. Causal/diagnostic questions are escalated to humans.
4. Weather metrics apply only to single-store single-date lookups.

---

## 7. Prioritised Iteration-2 Backlog
- **Priority 1: Multi-Day Trend & Growth Analysis** (Period-over-period revenue/footfall trends).
- **Priority 2: Multi-Turn Follow-Up Depth** (Context-aware pronouns and comparative sessions).
- **Priority 3: Hosted Cloud Database** (PostgreSQL/Supabase connection pooling with fallback retries).
