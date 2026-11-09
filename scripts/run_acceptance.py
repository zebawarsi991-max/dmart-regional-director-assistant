import os
import json
from agent.run_agent import handle

CASES = [
    {"id": "A01", "session": "s1", "question": "What was Pune's revenue on 15 May 2026?"},
    {"id": "A02", "session": "s1", "question": "And the target?"},
    {"id": "A03", "session": "s1", "question": "How about Mumbai?"},
    {"id": "A04", "session": "s2", "question": "How is Hyderabad doing?"},
    {"id": "A05", "session": "s2", "question": "revenue on 2026-05-15"},
    {"id": "A06", "session": "s3", "question": "What was Hydrabad's turnover yesterday?"},
    {"id": "A07", "session": "s4", "question": "Did Pune hit its target on 2026-05-16?"},
    {"id": "A08", "session": "s4", "question": "Did Pune hit its target on 2026-05-20?"},
    {"id": "A09", "session": "s4", "question": "Did Mumbai hit its target on 2026-05-21?"},
    {"id": "A10", "session": "s5", "question": "Which store had the highest average revenue between 2026-05-01 and 2026-05-31?"},
    {"id": "A11", "session": "s5", "question": "Which store had the lowest revenue on 2026-06-10?"},
    {"id": "A12", "session": "s6", "question": "Which stores are below the reorder threshold for Amul Milk?"},
    {"id": "A13", "session": "s6", "question": "What are customers saying about Hyderabad?"},
    {"id": "A14", "session": "s7", "question": "What was Pune's profit margin on 2026-05-15?"},
    {"id": "A15", "session": "s8", "question": "What is the capital of India?"},
    {"id": "A16", "session": "s9", "question": "What was Mumbai's revenue on 2026-07-15?"},
    {"id": "A17", "session": "s10", "question": "Why is Pune's revenue so low?"},
    {"id": "A18", "session": "s11", "question": "What was Kolkata's revenue on 2026-05-15?"},
    {"id": "A19", "session": "s12", "question": "What was Pune's revenue on 15 May 2026?", "sim_fail": 2},
    {"id": "A20", "session": "s13", "question": "What was Pune's revenue on 15 May 2026?", "sim_fail": 3}
]

def run_acceptance():
    os.environ["AGENT_LOG_PATH"] = "logs/runs.jsonl"
    if os.path.exists("logs/runs.jsonl"):
        os.remove("logs/runs.jsonl")
    os.makedirs("outputs", exist_ok=True)
    
    transcript_lines = ["# Acceptance Transcript\n"]
    
    for c in CASES:
        if "sim_fail" in c:
            os.environ["SIMULATE_DB_FAILURES"] = str(c["sim_fail"])
        else:
            os.environ["SIMULATE_DB_FAILURES"] = "0"
            
        res = handle(c["question"], session_id=c["session"])
        
        transcript_lines.append(f"### Case {c['id']} (Session {c['session']})")
        transcript_lines.append(f"- **Question:** {c['question']}")
        transcript_lines.append(f"- **Status:** {res['status']}")
        transcript_lines.append(f"- **Intent:** {res['intent']}")
        transcript_lines.append(f"- **Confidence:** {res['confidence']}")
        transcript_lines.append(f"- **Route:** {res['route']}")
        transcript_lines.append(f"- **Attempts:** {res['attempts']}")
        transcript_lines.append(f"- **Answer:** {res['answer_text']}\n")
        
    with open("outputs/acceptance_transcript.md", "w") as f:
        f.write("\n".join(transcript_lines))
        
    print("Acceptance test run complete. Transcript saved to outputs/acceptance_transcript.md and logs/runs.jsonl generated.")

if __name__ == "__main__":
    run_acceptance()
  Acceptance test run complete. Transcript saved to outputs/acceptance_transcript.md and logs/runs.jsonl generated.
