#!/usr/bin/env python3
"""
LegalLens 2.0 - Baseline Heuristic Agent
A simple rule-based agent that works through the environment action by action.
Can be used as a baseline for comparison with LLM agents.
"""

from __future__ import annotations

import sys
import os
from typing import Any, Dict, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from environment.env import LegalLensEnv


class BaselineAgent:
    """
    Heuristic baseline agent for LegalLens 2.0.
    Executes a fixed sequence of reasonable actions per task type.
    Does not use an LLM — serves as baseline comparison.
    """

    TASK_SCRIPTS: Dict[str, List[Dict[str, Any]]] = {
        "cyber_fraud": [
            {"action_type": "CLASSIFY_DOMAIN", "domain": "cyber_law"},
            {"action_type": "IDENTIFY_ISSUE", "issue": "Online phishing and financial fraud through fake banking portal"},
            {"action_type": "IDENTIFY_ISSUE", "issue": "Unauthorized digital transaction and identity impersonation"},
            {"action_type": "IDENTIFY_LAW", "law_id": "it_act_sec66d"},
            {"action_type": "IDENTIFY_LAW", "law_id": "bns_sec318"},
            {"action_type": "IDENTIFY_LAW", "law_id": "cyber_crime_portal"},
            {"action_type": "CHECK_JURISDICTION", "jurisdiction": "Cyber Crime Police Station, Bengaluru", "court": "Cyber Crime Portal / Police"},
            {"action_type": "REQUEST_EVIDENCE", "evidence_type": "DIGITAL_RECORD", "notes": "Screenshots of phishing WhatsApp message and fraudulent link"},
            {"action_type": "REQUEST_EVIDENCE", "evidence_type": "TRANSACTION", "notes": "Bank statements showing unauthorized debits of Rs 85,000"},
            {"action_type": "REQUEST_EVIDENCE", "evidence_type": "COMMUNICATION", "notes": "All communications with the fraudster"},
            {"action_type": "RECOMMEND_ACTION", "action_recommendation": "Immediately report to Cyber Crime Helpline 1930 and cybercrime.gov.in portal"},
            {"action_type": "RECOMMEND_ACTION", "action_recommendation": "Contact HDFC Bank immediately to freeze account and dispute transactions"},
            {"action_type": "RECOMMEND_ACTION", "action_recommendation": "File FIR at local police station under IT Act §66D and BNS §318"},
            {"action_type": "FINALIZE_ANALYSIS", "final_analysis": "This is a cyber fraud case under IT Act 2000 §66D (cheating by personation via computer) and BNS 2023 §318 (cheating). Victim should: (1) Call 1930 immediately, (2) Report on cybercrime.gov.in, (3) Contact bank to freeze account and reverse transactions, (4) File FIR at cyber crime police station. Evidence to preserve: bank statements, screenshots, WhatsApp messages.", "confidence": 0.85},
        ],
        "bail": [
            {"action_type": "CLASSIFY_DOMAIN", "domain": "criminal_law"},
            {"action_type": "IDENTIFY_ISSUE", "issue": "Arrest in alleged financial irregularities case"},
            {"action_type": "IDENTIFY_ISSUE", "issue": "Determination of bail eligibility — nature of offence unclear"},
            {"action_type": "IDENTIFY_LAW", "law_id": "bnss_sec480"},
            {"action_type": "IDENTIFY_LAW", "law_id": "bnss_sec482"},
            {"action_type": "IDENTIFY_LAW", "law_id": "bnss_sec483"},
            {"action_type": "ASK_CLARIFICATION",
             "question": "What specific sections/charges have been invoked? Is this a bailable or non-bailable offence?",
             "missing_info": [
                 "exact sections and charges filed",
                 "bailable or non-bailable classification",
                 "current procedural stage (FIR/arrest memo/chargesheet)",
                 "availability of supporting documents (company records, financial statements)",
                 "identity and designation of arresting officer",
             ]},
            {"action_type": "CHECK_JURISDICTION", "jurisdiction": "Mumbai", "court": "Magistrate Court / Sessions Court, Mumbai"},
            {"action_type": "REQUEST_EVIDENCE", "evidence_type": "DOCUMENT", "notes": "Arrest memo and FIR copy"},
            {"action_type": "REQUEST_EVIDENCE", "evidence_type": "OFFICIAL_RECORD", "notes": "Copy of sections invoked and remand order"},
            {"action_type": "RECOMMEND_ACTION", "action_recommendation": "Immediately obtain copy of FIR and arrest memo to identify specific charges"},
            {"action_type": "RECOMMEND_ACTION", "action_recommendation": "Engage criminal defense lawyer to appear before magistrate within 24 hours"},
            {"action_type": "RECOMMEND_ACTION", "action_recommendation": "If non-bailable offence, prepare bail application under BNSS §482/483 before Sessions Court or High Court"},
            {"action_type": "FINALIZE_ANALYSIS", "final_analysis": "CRITICAL MISSING INFORMATION: The exact charges/sections are unknown, making it impossible to definitively determine bail eligibility. If bailable offence (BNSS §480): bail is a right. If non-bailable (BNSS §482): application to Magistrate/Sessions Court required. Immediate steps: (1) Obtain FIR copy, (2) Identify specific charges, (3) Engage criminal lawyer, (4) Appear before magistrate within 24 hours of arrest as required by law.", "confidence": 0.65},
        ],
        "consumer": [
            {"action_type": "CLASSIFY_DOMAIN", "domain": "consumer_law"},
            {"action_type": "IDENTIFY_ISSUE", "issue": "Defective product (refrigerator) failing under warranty within 45 days"},
            {"action_type": "IDENTIFY_ISSUE", "issue": "Deficiency of service by seller and manufacturer in refusing replacement/refund"},
            {"action_type": "IDENTIFY_LAW", "law_id": "cpa_2019_sec2"},
            {"action_type": "IDENTIFY_LAW", "law_id": "cpa_2019_sec35"},
            {"action_type": "IDENTIFY_LAW", "law_id": "cpa_2019_remedies"},
            {"action_type": "IDENTIFY_LAW", "law_id": "cpa_2019_sec69"},
            {"action_type": "CHECK_JURISDICTION", "jurisdiction": "Pune, Maharashtra", "court": "District Consumer Disputes Redressal Commission, Pune"},
            {"action_type": "REQUEST_EVIDENCE", "evidence_type": "DOCUMENT", "notes": "Original purchase invoice and warranty card"},
            {"action_type": "REQUEST_EVIDENCE", "evidence_type": "COMMUNICATION", "notes": "All service request communications, technician visit reports"},
            {"action_type": "REQUEST_EVIDENCE", "evidence_type": "PHOTOGRAPH", "notes": "Photographs of defective refrigerator"},
            {"action_type": "RECOMMEND_ACTION", "action_recommendation": "File consumer complaint before District Consumer Disputes Redressal Commission, Pune"},
            {"action_type": "RECOMMEND_ACTION", "action_recommendation": "Claim full refund of Rs 28,500 plus compensation for inconvenience under CPA 2019 §39"},
            {"action_type": "RECOMMEND_ACTION", "action_recommendation": "File within the 2-year limitation period (before January 2026 from purchase date)"},
            {"action_type": "FINALIZE_ANALYSIS", "final_analysis": "Consumer dispute under Consumer Protection Act 2019. Anil qualifies as a consumer. Product defect within warranty = deficiency of service. Appropriate forum: District Consumer Disputes Redressal Commission, Pune (value Rs 28,500 < Rs 1 crore limit). Remedies available: full refund, replacement, compensation. Limitation: 2 years from cause of action (last rejection: 10 March 2024). File immediately with: invoice, warranty card, service records, rejection letter, photographs.", "confidence": 0.90},
        ],
        "property": [
            {"action_type": "CLASSIFY_DOMAIN", "domain": "property_law"},
            {"action_type": "IDENTIFY_ISSUE", "issue": "Fraudulent double-sale of immovable property (Plot 42, Noida)"},
            {"action_type": "IDENTIFY_ISSUE", "issue": "Wrongful possession and construction by fraudulent purchaser"},
            {"action_type": "IDENTIFY_LAW", "law_id": "tpa_1882_sec54"},
            {"action_type": "IDENTIFY_LAW", "law_id": "specific_relief_act_sec6"},
            {"action_type": "IDENTIFY_LAW", "law_id": "specific_relief_act_sec34"},
            {"action_type": "IDENTIFY_LAW", "law_id": "registration_act_1908"},
            {"action_type": "ASK_CLARIFICATION",
             "question": "How did Vijay Singh obtain any right to sell the property if Suresh had registered title since 2010?",
             "missing_info": [
                 "chain of title from Vijay Singh",
                 "encumbrance certificate for the plot",
                 "mortgage or lien status",
                 "how Ramesh Kumar's sale deed was registered despite existing title",
             ]},
            {"action_type": "CHECK_JURISDICTION", "jurisdiction": "Noida, Uttar Pradesh", "court": "Civil Court, Noida / District Court, Gautam Buddha Nagar"},
            {"action_type": "REQUEST_EVIDENCE", "evidence_type": "DOCUMENT", "notes": "Original registered sale deed (2010) from Sub-Registrar, Noida"},
            {"action_type": "REQUEST_EVIDENCE", "evidence_type": "OFFICIAL_RECORD", "notes": "Encumbrance certificate for Plot 42, Sector 7, Noida"},
            {"action_type": "REQUEST_EVIDENCE", "evidence_type": "FINANCIAL_RECORD", "notes": "Property tax receipts 2010-2023 in Suresh's name"},
            {"action_type": "REQUEST_EVIDENCE", "evidence_type": "PHOTOGRAPH", "notes": "Photographs showing unauthorized construction"},
            {"action_type": "RECOMMEND_ACTION", "action_recommendation": "File for interim injunction to immediately stop construction on Plot 42"},
            {"action_type": "RECOMMEND_ACTION", "action_recommendation": "File declaration of title suit under Specific Relief Act §34 in Civil Court, Noida"},
            {"action_type": "RECOMMEND_ACTION", "action_recommendation": "File FIR for fraud against Vijay Singh and Ramesh Kumar under BNS §318"},
            {"action_type": "FINALIZE_ANALYSIS", "final_analysis": "Property fraud case: fraudulent double-sale of Plot 42, Noida. Suresh has registered title since 2010 supported by tax receipts and utility connections. Priority: (1) Seek urgent interim injunction to stop construction, (2) File civil suit for declaration of title under SRA §34, (3) File FIR for criminal fraud, (4) Obtain encumbrance certificate to trace fraudulent sale. Key missing info: how Vijay Singh obtained selling rights. Suresh's 2010 registered deed creates strong prima facie title.", "confidence": 0.75},
        ],
    }

    def run(self, task_id: str = "cyber_fraud", max_steps: int = 20) -> Dict[str, Any]:
        """Run the baseline agent on a task and return results."""
        env = LegalLensEnv()
        obs = env.reset(task_id=task_id)

        script = self.TASK_SCRIPTS.get(task_id, self.TASK_SCRIPTS["cyber_fraud"])
        steps_log = []
        rewards = []

        for i, action in enumerate(script[:max_steps]):
            if obs.done:
                break
            result = env.step(action)
            step_log = {
                "step": i + 1,
                "action": action.get("action_type"),
                "reward": result.reward,
                "done": result.done,
                "result": result.observation.last_action_result,
                "error": result.error,
            }
            steps_log.append(step_log)
            rewards.append(result.reward)
            obs = result.observation

        ep = env.episode_result()
        return {
            "task_id": task_id,
            "steps": steps_log,
            "rewards": rewards,
            "total_reward": round(sum(rewards), 4),
            "final_score": ep.final_score if ep else 0.0,
            "success": ep.success if ep else False,
            "total_steps": len(steps_log),
            "grader_breakdown": ep.grader_breakdown if ep else {},
            "feedback": ep.feedback if ep else "",
            "final_analysis": ep.final_analysis if ep else None,
        }


def main():
    """CLI entry point for running baseline agent."""
    import json
    task_id = sys.argv[1] if len(sys.argv) > 1 else "cyber_fraud"
    print(f"[BASELINE] Running task: {task_id}", file=sys.stderr)
    agent = BaselineAgent()
    result = agent.run(task_id=task_id)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
