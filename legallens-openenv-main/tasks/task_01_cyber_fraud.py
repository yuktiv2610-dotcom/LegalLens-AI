"""
LegalLens 2.0 - Task 01: Cyber Fraud / Online Financial Fraud
"""

from .task_definitions import TaskDefinition

CYBER_FRAUD_FACTS = """
CASE FACTS:
Priya Sharma, a resident of Bengaluru, received a WhatsApp message from an unknown number 
claiming to be a representative of her bank (HDFC Bank). The message stated that her 
bank account would be suspended within 24 hours unless she verifies her KYC details immediately 
by clicking a provided link.

Priya clicked the link, which appeared identical to the bank's official website. She entered 
her debit card number, CVV, and OTP received on her phone. Within minutes, Rs 85,000 was 
debited from her account in three transactions to an unknown beneficiary.

Timeline:
- Incident date: 15 March 2024
- Amount lost: Rs 85,000 (3 transactions)
- Transactions via: UPI/IMPS
- Priya still has: bank statements, screenshots of the WhatsApp message, and the fraudulent link

She has not yet reported to police or the cyber crime portal.
It has been 2 days since the incident.

Question: What legal options are available to Priya? What should she do immediately?
"""

TASK_CYBER_FRAUD = TaskDefinition(
    id="cyber_fraud",
    name="Cyber Fraud Investigation",
    description="A victim of online banking fraud through phishing needs legal guidance on immediate steps, applicable laws, and remedies.",
    domain="cyber_law",
    difficulty=2,
    facts=CYBER_FRAUD_FACTS,
    max_steps=20,
    gold_standard={
        "correct_domain": "cyber_law",
        "relevant_issue_keywords": [
            "phishing", "online fraud", "unauthorized transaction", "impersonation",
            "KYC fraud", "financial fraud", "cheating", "identity theft"
        ],
        "relevant_law_ids": [
            "it_act_sec66d",
            "it_act_sec66",
            "bns_sec318",
            "cyber_crime_portal",
            "it_act_sec43",
        ],
        "correct_jurisdiction_keywords": [
            "cyber crime", "police", "bengaluru", "karnataka", "1930", "cybercrime.gov.in"
        ],
        "relevant_evidence_types": [
            "DIGITAL_RECORD", "TRANSACTION", "COMMUNICATION", "DOCUMENT", "FINANCIAL_RECORD"
        ],
        "correct_action_keywords": [
            "report", "cyber crime portal", "1930", "bank", "freeze", "FIR",
            "block card", "helpline", "police complaint"
        ],
        "facts_are_incomplete": False,
    },
    hints=[
        "Consider both IT Act and BNS provisions",
        "Time is critical — cyber fraud victims should act within 24-48 hours",
        "The National Cyber Crime Portal (cybercrime.gov.in) and helpline 1930 are key",
        "Bank must be notified immediately to freeze transactions",
    ],
    tags=["cyber", "fraud", "phishing", "financial", "urgent"],
)
