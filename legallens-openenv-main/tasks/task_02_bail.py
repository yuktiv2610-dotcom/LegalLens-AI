"""
LegalLens 2.0 - Task 02: Bail Application / Criminal Procedure
Facts are deliberately incomplete — agent should identify missing information.
"""

from .task_definitions import TaskDefinition

BAIL_FACTS = """
CASE FACTS:
Rajan Mehta has been arrested by the Mumbai Police in connection with an alleged case 
involving financial irregularities at his company. His family has contacted a lawyer.

Known facts:
- Rajan was arrested yesterday and is currently in police custody
- The arrest was made without a warrant (claimed to be under cognizable offence provisions)
- The family reports the alleged amount involved is approximately Rs 2 crore
- Rajan has no prior criminal record according to his family
- His company has 45 employees

Unknown/Unclear:
- The exact sections/offences he has been charged with are NOT yet known
- It is not clear whether the offence is bailable or non-bailable
- The current procedural stage (whether chargesheet has been filed) is unclear
- Available documents (if any) for bail application are unknown
- The relevant magistrate/court has not been identified

Question: What procedural options are available for Rajan's bail? 
What information is urgently needed to determine the appropriate legal route?
"""

TASK_BAIL = TaskDefinition(
    id="bail",
    name="Bail Application & Criminal Procedure",
    description="A person has been arrested and the family needs guidance on bail options. Facts are deliberately incomplete to test whether the agent can identify missing critical information.",
    domain="criminal_law",
    difficulty=4,
    facts=BAIL_FACTS,
    max_steps=20,
    gold_standard={
        "correct_domain": "criminal_law",
        "relevant_issue_keywords": [
            "bail", "arrest", "custody", "non-bailable", "bailable",
            "procedural", "charge", "financial irregularity"
        ],
        "relevant_law_ids": [
            "bnss_sec482",
            "bnss_sec480",
            "bnss_sec483",
            "bnss_anticipatory_bail",
        ],
        "correct_jurisdiction_keywords": [
            "mumbai", "magistrate", "sessions court", "high court", "bombay"
        ],
        "relevant_evidence_types": [
            "DOCUMENT", "OFFICIAL_RECORD", "FINANCIAL_RECORD", "COMPLAINT"
        ],
        "correct_action_keywords": [
            "bail application", "magistrate", "sessions", "surety",
            "sections", "charge", "identify offence", "lawyer"
        ],
        "facts_are_incomplete": True,  # KEY: agent should flag missing information
        "required_missing_info": [
            "exact sections/charges",
            "bailable or non-bailable",
            "procedural stage",
            "chargesheet",
            "supporting documents",
        ],
    },
    hints=[
        "The exact charges are not known — this is intentional",
        "An agent should flag: 'Cannot determine bail type without knowing specific charges'",
        "Recognizing uncertainty is rewarded more than guessing wrong",
        "Both BNSS §480 (bailable) and §482 (non-bailable) may be relevant depending on charges",
    ],
    tags=["bail", "criminal", "procedure", "arrest", "uncertainty"],
)
