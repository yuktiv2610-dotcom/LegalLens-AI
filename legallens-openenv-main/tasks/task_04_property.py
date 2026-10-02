"""
LegalLens 2.0 - Task 04: Property Dispute / Title and Possession
"""

from .task_definitions import TaskDefinition

PROPERTY_FACTS = """
CASE FACTS:
Suresh Nair owns a residential plot (Plot No. 42, Sector 7, Noida, Uttar Pradesh) 
which he purchased in 2010 for Rs 15 lakh. He has the original registered sale deed in his name.

Problem:
In January 2024, Suresh discovered that:
1. An individual named "Ramesh Kumar" claims to have purchased the same plot from a 
   third party ("Vijay Singh") in November 2023 for Rs 25 lakh
2. Ramesh Kumar has obtained what appears to be a registered sale deed for the same property
3. Ramesh Kumar has begun construction on the plot without Suresh's knowledge or consent
4. When Suresh confronted Ramesh, he was told the original 2010 sale was fraudulent

Available documents (Suresh has):
- Original registered sale deed (2010, registered at Sub-Registrar, Noida)
- Property tax receipts in his name (2010-2023)
- Electricity connection in his name
- Photographs of the plot before the disputed construction

Unknown:
- How Vijay Singh obtained any rights to sell the property
- Whether any encumbrance certificate was checked
- Current status of any loan or mortgage on the property

Question: What legal remedies are available to Suresh? What are the priority actions?
"""

TASK_PROPERTY = TaskDefinition(
    id="property",
    name="Property Dispute - Title & Possession",
    description="A fraudulent double-sale of property has occurred. The original owner needs guidance on legal remedies to protect title and possession. Tests knowledge of property law, civil remedies, and documentation requirements.",
    domain="property_law",
    difficulty=4,
    facts=PROPERTY_FACTS,
    max_steps=20,
    gold_standard={
        "correct_domain": "property_law",
        "relevant_issue_keywords": [
            "fraudulent sale", "double sale", "title", "possession", "dispossession",
            "registered sale deed", "property dispute", "encumbrance"
        ],
        "relevant_law_ids": [
            "tpa_1882_sec54",
            "specific_relief_act_sec6",
            "specific_relief_act_sec34",
            "registration_act_1908",
            "limitation_act_sec3",
        ],
        "correct_jurisdiction_keywords": [
            "civil court", "noida", "uttar pradesh", "district court",
            "sub-registrar", "civil judge"
        ],
        "relevant_evidence_types": [
            "DOCUMENT", "OFFICIAL_RECORD", "PHOTOGRAPH", "FINANCIAL_RECORD"
        ],
        "correct_action_keywords": [
            "injunction", "civil suit", "title", "declaration", "possession",
            "police complaint", "FIR", "civil court", "encumbrance certificate"
        ],
        "facts_are_incomplete": True,  # Info about Vijay Singh's title is unknown
        "required_missing_info": [
            "how Vijay Singh obtained rights",
            "encumbrance certificate",
            "mortgage status",
            "chain of title",
        ],
    },
    hints=[
        "Priority: Seek interim injunction to stop construction immediately",
        "Original registered sale deed (2010) is strong evidence of title",
        "File FIR for fraud under BNS §318 + property-specific offences",
        "Declaration of title suit under Specific Relief Act §34",
        "Agent should note missing chain of title information",
    ],
    tags=["property", "title", "fraud", "possession", "civil", "injunction"],
)
