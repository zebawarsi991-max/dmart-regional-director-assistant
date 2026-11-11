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
- **Status:** Drafted
- **Intent:** target_vs_actual
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 1
- **Answer:** Pune on 2026-05-15: revenue INR 623845.00, target INR 900000.00, achievement 69.32%, performance band Poor.

### Case A03 (Session s1)
- **Question:** How about Mumbai?
- **Status:** Answered
- **Intent:** target_vs_actual
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 1
- **Answer:** Mumbai on 2026-05-15: revenue INR 1093374.78, target INR 1050000.00, achievement 104.13%, performance band Excellent.

### Case A04 (Session s2)
- **Question:** How is Hyderabad doing?
- **Status:** Answered
- **Intent:** lookup
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 1
- **Answer:** Hyderabad's revenue_inr on 2026-05-15 was INR 786399.27.

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
- **Confidence:** 0.94
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
- **Answer:** Pune on 2026-05-16: revenue INR 671332.65, target INR 900000.00, achievement 74.59%, performance band Poor.

### Case A08 (Session s4)
- **Question:** Did Pune hit its target on 2026-05-20?
- **Status:** Answered
- **Intent:** target_vs_actual
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 1
- **Answer:** Pune on 2026-05-20: revenue INR 677739.77, target INR 900000.00, achievement 75.30%, performance band Good.

### Case A09 (Session s4)
- **Question:** Did Mumbai hit its target on 2026-05-21?
- **Status:** Answered
- **Intent:** target_vs_actual
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 1
- **Answer:** Mumbai on 2026-05-21: revenue INR 1133910.49, target INR 1050000.00, achievement 107.99%, performance band Excellent.

### Case A10 (Session s5)
- **Question:** Which store had the highest average revenue between 2026-05-01 and 2026-05-31?
- **Status:** Answered
- **Intent:** comparison
- **Confidence:** 1.0
- **Route:** sql
- **Attempts:** 1
- **Answer:** Comparison results for revenue_inr: Mumbai INR 1136170.63; Hyderabad INR 942985.17; Bengaluru INR 870079.50; Ahmedabad INR 758157.69; Pune INR 592241.72.

### Case A11 (Session s5)
- **Question:** Which store had the lowest revenue on 2026-06-10?
- **Status:** Answered
- **Intent:** comparison
- **Confidence:** 1.0
- **Route:** sql
- **Attempts:** 1
- **Answer:** Comparison results for revenue_inr: Mumbai INR 903822.34; Bengaluru INR 848248.05; Ahmedabad INR 819290.32; Hyderabad INR 807522.21; Pune INR 602942.85.

### Case A12 (Session s6)
- **Question:** Which stores are below the reorder threshold for Amul Milk?
- **Status:** Answered
- **Intent:** inventory
- **Confidence:** 1.0
- **Route:** sql
- **Attempts:** 1
- **Answer:** No store is below its reorder threshold for Amul Milk.

### Case A13 (Session s6)
- **Question:** What are customers saying about Hyderabad?
- **Status:** Answered
- **Intent:** feedback
- **Confidence:** 1.0
- **Route:** sql
- **Attempts:** 1
- **Answer:** Customer feedback for Hyderabad: average rating 2.63, 38 rated of 40, most frequent theme Stock availability.

### Case A14 (Session s7)
- **Question:** What was Pune's profit margin on 2026-05-15?
- **Status:** Safe Failure
- **Intent:** unsupported_metric
- **Confidence:** 1.0
- **Route:** none
- **Attempts:** 0
- **Answer:** Pre-query validation or clarification needed.

### Case A15 (Session s8)
- **Question:** What is the capital of India?
- **Status:** Clarification Needed
- **Intent:** lookup
- **Confidence:** 0.4
- **Route:** none
- **Attempts:** 0
- **Answer:** Clarification needed: Confidence is below 0.7 or missing required entities (store, metric, date). Please clarify.

### Case A16 (Session s9)
- **Question:** What was Mumbai's revenue on 2026-07-15?
- **Status:** Safe Failure
- **Intent:** lookup
- **Confidence:** 1.0
- **Route:** python
- **Attempts:** 0
- **Answer:** Date out of range. Available range is 2026-04-01 to 2026-06-29.

### Case A17 (Session s10)
- **Question:** Why is Pune's revenue so low?
- **Status:** Escalated
- **Intent:** diagnostic
- **Confidence:** 1.0
- **Route:** none
- **Attempts:** 0
- **Answer:** This request is out of scope or diagnostic. An analyst or escalation is required.

### Case A18 (Session s11)
- **Question:** What was Kolkata's revenue on 2026-05-15?
- **Status:** Clarification Needed
- **Intent:** lookup
- **Confidence:** 0.4
- **Route:** none
- **Attempts:** 0
- **Answer:** Clarification needed: Confidence is below 0.7 or missing required entities (store). Please clarify.

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
