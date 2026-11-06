Agent Specification: DMart Regional Director Assistant

Skeleton: tables and rules follow the brief. Rewrite every "Why / note" cell and every sentence marked [YOUR WORDS] in your own words. Keep the numbers, thresholds and status names exactly as they are.

1. Pipeline
#	Step	What it does	Deterministic or generative	Technique
1	Interpret	Turns the question into intent, store, metric, date or range, product, weather flag, confidence and missing entities	Generative	Rule-based interpreter, no language model
2	Route	Chooses the Python function, the SQL query, the weather tool, or no route	Deterministic	Rule lookup on the intent
3	Query	Runs the data query and retries a failed one (max 3 attempts)	Deterministic	Python function or SQLite with ? parameters
4	Validate	Checks the table and columns against the 11 approved fields	Deterministic	Whitelist check
5	Calculate	Averages, ranking, achievement and band	Deterministic	Integer-cent sums and decimal ROUND_HALF_UP
6	Synthesize	Writes the reply text	Generative	Fixed answer templates, no language model
7	Ground	Builds evidence and grounded_values, counts ungrounded_numbers	Deterministic	Values taken from fetched data, never by scanning the final text
8	Record	Appends one JSON line to the log	Deterministic	Log path read from AGENT_LOG_PATH on every call

Position of Validate. [YOUR WORDS: Validate is listed fourth, but it runs after the query is built and before it executes. A failed check stops the pipeline and no query runs.]

2. Intents
Intent	Example question	Route
lookup	What was Pune's revenue on 15 May 2026?	Python function (one store, one date); SQL (a range, returns the average)
target_vs_actual	Did Pune hit its target on 2026-05-16?	Python function
comparison	Which store had the highest average revenue between 2026-05-01 and 2026-05-31?	SQL
inventory	Which stores are below the reorder threshold for Amul Milk?	SQL
feedback	What are customers saying about Hyderabad?	SQL
weather	What was the weather in Pune on 2026-05-16?	Weather tool
unsupported_metric	What was Pune's profit margin on 2026-05-15?	None
out_of_scope	What is the capital of India?	None
diagnostic	Why is Pune's revenue so low?	None

A weather word together with a metric adds the weather to a lookup or target_vs_actual for one store and one date (route python+weather). For a comparison, inventory, feedback or a range lookup the weather word is ignored and the tool is not called.

Intent order (the first rule that applies decides)
A request to ignore or override the rules, or to take a prohibited action (send, email, restock, place an order, imperative reorder and the other listed words) is out_of_scope, even if it names a metric, store or date.
A column outside the approved 11 (profit, margin, marketing, cost, expense, shortfall, efficiency, weekend, per footfall, per visitor) is unsupported_metric.
A why, trend or reason question is diagnostic.
A product name, or the words reorder or inventory, is inventory.
Feedback, reviews, ratings, or customers saying, is feedback.
The word target with hit, met, miss, beat, reach, below, above, against, versus and similar words, or achievement, or performance band, is target_vs_actual.
A which, highest, lowest, best or worst question that names no store is comparison.
A metric, with or without a store and date, is lookup.
A weather word with no metric is weather.
A store and/or a date (resolved or unresolved) with no metric and no weather word is lookup, or target_vs_actual if the session's last stored question was target_vs_actual.
Nothing recognisable is out_of_scope.
3. Handling rules
Stores
Exact name, case-insensitive: confidence 1.0.
Bangalore is an alias of Bengaluru: confidence 1.0.
A misspelling is matched by fuzzy similarity against the five store names; the best score is the confidence. Only candidate words are fuzzy-matched (5+ letters, capitalised or with 's, not the first word unless it has 's, not a keyword or stop word).
A candidate below 0.7 in the cases Part C lists is an unresolved named store: confidence 0.4, never filled from context.
[YOUR WORDS: one sentence on why a lowercase misspelling is not matched.]
Metric synonyms (closed list)
Word	Field
revenue, sales, turnover, earnings	revenue_inr
target	daily_target_inr
footfall, visitors	footfall
stockout	stockout_hours
discount	discount_pct
Dates (closed grammar)
YYYY-MM-DD (exactly four digits, two, two, and a real calendar date).
D Month YYYY with the full month name.
yesterday.
between <date> and <date>, inclusive.
AS_OF_DATE = 2026-06-30, so yesterday is 2026-06-29.
Anything else that looks like a date is an unresolved named date (confidence 0.4, Clarification Needed, never filled from context).
A range given to target_vs_actual or weather is an unresolved named date.
Data range: 2026-04-01 to 2026-06-29.
Confidence
Confidence is the minimum over the entities the intent uses.
1.0: exact store, alias, exact product, synonym, any date resolved by the grammar.
Fuzzy similarity: a fuzzy store match.
0.4: a missing required entity, an unresolved named store or date, or an ambiguous question.
Two different stores or two different metrics among the used entities: confidence 0.4, ask which one.
Clarification threshold: 0.7. Below it the agent asks and does not answer.
A question with no entities has confidence 1.0; a value from context counts as 1.0.
Session context
An entity named in the new question overrides the old one.
A missing required entity is taken from the last resolved value in the same session; only required entities are taken.
An unresolved named store or date and an ambiguous pair are never replaced from context.
A range in context is never carried into a single-date intent.
Context never crosses sessions.
unsupported_metric, diagnostic and out_of_scope do not update context; every other question stores the used entities it resolved.
A target_vs_actual question stores store and date only, and marks the session so a bare store or date follow-up means target_vs_actual again.
Entities used per intent
Intent	Required	Optional
lookup	store, metric, date or range	none
target_vs_actual	store, one date	none
comparison	metric, date or range	none
inventory	product	store
feedback	store	none
weather	store, one date	none
unsupported_metric, out_of_scope, diagnostic	none	none

Anything else mentioned is dropped before validation.

4. Status decision table
Status	Exact condition
Answered	Understood, fetched, validated and grounded, and no alert fired
Drafted	Answer composed but held for human approval because a target_vs_actual result is in the Poor band (below 75% of target)
Clarification Needed	Confidence below 0.7, a required entity missing, an unresolved named store or date, or two different stores or metrics
Escalated	Out of scope, a diagnostic question, or 3 failed attempts
Safe Failure	A field outside the approved list, a date outside 2026-04-01 to 2026-06-29, or no record found (no row for the product, store or date)
Precedence (the first rule that applies decides)
Intent: unsupported_metric is Safe Failure; out_of_scope and diagnostic are Escalated.
A required entity missing, an unresolved named store or date, two different stores or metrics, or confidence below 0.7 is Clarification Needed.
For lookup, target_vs_actual, comparison and weather: a date or range outside the data range is Safe Failure (inventory and feedback drop dates).
Data queries: 3 failed attempts is Escalated; no record found is Safe Failure.
Otherwise Drafted if the alert fired, else Answered.
5. Escalation and retry rules
A data query gets at most three attempts (the first try plus two retries).
After the third failure the status is Escalated.
attempts in the log is the highest attempt count among the question's data queries, and 0 when no data query runs.
A retry is not an extra tool_calls entry.
Out-of-scope and diagnostic questions are Escalated without any query.
Testing hook: SIMULATE_DB_FAILURES=<n> makes the first n attempts of every query fail.
6. Success criteria
Criterion	How it is measured
Every number in a reply comes from fetched data	ungrounded_numbers is 0 on every log line
One log line per question with every required key	Line count and keys in the run log
Approved fields checked before every query	Code read; unsupported fields give Safe Failure
No user text joined into SQL	Values are ? parameters; column names only from the whitelist
The 20 acceptance cases give the required status, intent and content	outputs/acceptance_transcript.md
Replies stay within budget	budget_exceeded is false (tokens_est at most 150)
No non-answer reply states an INR figure	Check on the eval run log
Weather tool only for weather questions	tools_called is empty when there is no weather word
7. Completion states and test categories

Every question ends in exactly one of five states: Answered, Drafted, Clarification Needed, Escalated, Safe Failure.

Part D test-case categories:

Intent-based: lookup, target_vs_actual, comparison, inventory, feedback, weather, diagnostic, retry.
Safety and edge cases: typo, synonym, ambiguity, unsupported_metric, out_of_scope, injection, out_of_range_date, unresolved_store, unresolved_date.
