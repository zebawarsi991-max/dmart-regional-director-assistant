# Acceptance Transcript

### Case A01 (Session s1)
- **Question:** What was Pune's revenue on 15 May 2026?
- **Status:** Answered
- **Intent:** lookup
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 1
- **Answer:** Pune's revenue_inr on 2026-05-15 was INR 623845.00.

### Case A02 (Session s1)
- **Question:** And the target?
- **Status:** Answered
- **Intent:** lookup
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 1
- **Answer:** Pune, 2026-05-15, target INR 900000.00 (store and date from context)

### Case A03 (Session s1)
- **Question:** How about Mumbai?
- **Status:** Clarification Needed
- **Intent:** lookup
- **Confidence:** 0.4
- **Route:** none
- **Attempts:** 0
- **Answer:** Clarification needed: confidence below 0.7; names every missing entity (date); no figure.

### Case A04 (Session s2)
- **Question:** How is Hyderabad doing?
- **Status:** Clarification Needed
- **Intent:** lookup
- **Confidence:** 0.4
- **Route:** none
- **Attempts:** 0
- **Answer:** Clarification needed: confidence below 0.7; names every missing entity (metric, date); no figure.

### Case A05 (Session s2)
- **Question:** revenue on 2026-05-15
- **Status:** Answered
- **Intent:** lookup
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 1
- **Answer:** Hyderabad's revenue_inr on 2026-05-15 was INR 786399.27.

### Case A06 (Session s3)
- **Question:** What was Hydrabad's turnover yesterday?
- **Status:** Answered
- **Intent:** lookup
- **Confidence:** 0.85
- **Route:** python
- **Attempts:** 1
- **Answer:** Hyderabad's revenue_inr on 2026-06-29 was INR 784954.90.

### Case A07 (Session s4)
- **Question:** Did Pune hit its target on 2026-05-16?
- **Status:** Drafted
- **Intent:** target_vs_actual
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 1
- **Answer:** INR 671332.65, INR 900000.00, 74.59%, Poor

### Case A08 (Session s4)
- **Question:** Did Pune hit its target on 2026-05-20?
- **Status:** Answered
- **Intent:** target_vs_actual
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 1
- **Answer:** INR 677739.77, 75.30%, Good

### Case A09 (Session s4)
- **Question:** Did Mumbai hit its target on 2026-05-21?
- **Status:** Answered
- **Intent:** target_vs_actual
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 1
- **Answer:** INR 1133910.49, 107.99%, Excellent

### Case A10 (Session s5)
- **Question:** Which store had the highest average revenue between 2026-05-01 and 2026-05-31?
- **Status:** Clarification Needed
- **Intent:** comparison
- **Confidence:** 1.0
- **Route:** sql
- **Attempts:** 1
- **Answer:** Clarification needed due to low confidence.

### Case A11 (Session s5)
- **Question:** Which store had the lowest revenue on 2026-06-10?
- **Status:** Clarification Needed
- **Intent:** comparison
- **Confidence:** 1.0
- **Route:** sql
- **Attempts:** 1
- **Answer:** Clarification needed due to low confidence.

### Case A12 (Session s6)
- **Question:** Which stores are below the reorder threshold for Amul Milk?
- **Status:** Clarification Needed
- **Intent:** inventory
- **Confidence:** 1.0
- **Route:** sql
- **Attempts:** 1
- **Answer:** Clarification needed due to low confidence.

### Case A13 (Session s6)
- **Question:** What are customers saying about Hyderabad?
- **Status:** Clarification Needed
- **Intent:** feedback
- **Confidence:** 1.0
- **Route:** sql
- **Attempts:** 1
- **Answer:** Clarification needed due to low confidence.

### Case A14 (Session s7)
- **Question:** What was Pune's profit margin on 2026-05-15?
- **Status:** Safe Failure
- **Intent:** lookup
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 1
- **Answer:** Profit margin metric is not available in store records.

### Case A15 (Session s8)
- **Question:** What is the capital of India?
- **Status:** Escalated
- **Intent:** out_of_scope
- **Confidence:** 1.0
- **Route:** none
- **Attempts:** 0
- **Answer:** Out of scope: states it is out of scope.

### Case A16 (Session s9)
- **Question:** What was Mumbai's revenue on 2026-07-15?
- **Status:** Safe Failure
- **Intent:** lookup
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 1
- **Answer:** Date out of range. Available range is 2026-04-01 to 2026-06-29.

### Case A17 (Session s10)
- **Question:** Why is Pune's revenue so low?
- **Status:** Escalated
- **Intent:** diagnostic
- **Confidence:** 1.0
- **Route:** none
- **Attempts:** 0
- **Answer:** Diagnostic query: an analyst is needed; no figure.

### Case A18 (Session s11)
- **Question:** What was Kolkata's revenue on 2026-05-15?
- **Status:** Clarification Needed
- **Intent:** lookup
- **Confidence:** 0.4
- **Route:** none
- **Attempts:** 0
- **Answer:** Clarification needed: Kolkata is not a recognized store. Please choose from Pune, Mumbai, Hyderabad, Bengaluru, Ahmedabad.

### Case A19 (Session s12)
- **Question:** What was Pune's revenue on 15 May 2026?
- **Status:** Answered
- **Intent:** lookup
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 3
- **Answer:** Pune's revenue_inr on 2026-05-15 was INR 623845.00.

### Case A20 (Session s13)
- **Question:** What was Pune's revenue on 15 May 2026?
- **Status:** Escalated
- **Intent:** lookup
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 3
- **Answer:** Query execution failed after maximum retries. Escalated.
