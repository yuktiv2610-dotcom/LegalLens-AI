"""
LegalLens 2.0 - Task 03: Consumer Dispute / Defective Product
"""

from .task_definitions import TaskDefinition

CONSUMER_FACTS = """
CASE FACTS:
Anil Kumar purchased a Samsung refrigerator (Model: RT28T3122S8) for Rs 28,500 from 
a local electronics shop "Cool Electronics" in Pune on 10 January 2024. The shop provided 
a 1-year warranty.

Problems:
- The refrigerator stopped cooling within 45 days of purchase (25 February 2024)
- Anil contacted the shop and Samsung's customer service multiple times
- A company technician visited but only provided a temporary fix — the problem recurred
- After 3 visits, the company refused to replace the product or provide a full refund
- They offered only a 30% refund as "depreciation deduction" despite the product being under 
  warranty and failing within 45 days

Current status (today: 15 March 2024):
- Last rejection of full refund: 10 March 2024
- Anil has: original invoice, warranty card, all service request numbers, 
  written communications with the company, photographs of the defective product
- Total value: Rs 28,500

Question: What legal remedy is available to Anil? Where and how should he file a complaint?
"""

TASK_CONSUMER = TaskDefinition(
    id="consumer",
    name="Consumer Dispute - Defective Product",
    description="A consumer with a defective product under warranty is being denied a full replacement/refund. Tests knowledge of consumer protection laws, appropriate forum, and available remedies.",
    domain="consumer_law",
    difficulty=2,
    facts=CONSUMER_FACTS,
    max_steps=20,
    gold_standard={
        "correct_domain": "consumer_law",
        "relevant_issue_keywords": [
            "defective product", "warranty", "deficiency of service", "refund",
            "replacement", "consumer dispute", "unfair trade practice"
        ],
        "relevant_law_ids": [
            "cpa_2019_sec35",
            "cpa_2019_sec2",
            "cpa_2019_remedies",
            "cpa_2019_sec69",
        ],
        "correct_jurisdiction_keywords": [
            "district", "consumer", "pune", "maharashtra", "district commission",
            "District Consumer Disputes Redressal Commission"
        ],
        "relevant_evidence_types": [
            "DOCUMENT", "COMMUNICATION", "OFFICIAL_RECORD", "PHOTOGRAPH", "CONTRACT"
        ],
        "correct_action_keywords": [
            "district commission", "consumer complaint", "refund", "replacement",
            "compensation", "file complaint", "within two years"
        ],
        "facts_are_incomplete": False,
    },
    hints=[
        "Value is Rs 28,500 — District Consumer Disputes Redressal Commission has jurisdiction (up to Rs 1 crore)",
        "The 2-year limitation period under CPA 2019 §69 applies",
        "Multiple service failures + warranty denial = deficiency of service",
        "Remedies include: repair, replacement, refund, and compensation",
    ],
    tags=["consumer", "product", "defective", "warranty", "refund", "district commission"],
)
