"""
LegalLens 2.0 - Indian Legal Knowledge Base.
Contains verified references to Indian statutes and regulations.
All references are marked VERIFIED or REQUIRES_VERIFICATION.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from environment.models import LawReference

# Canonical law database - verified Indian legal references
_LAWS: List[Dict] = [
    # =========================================================
    # CYBER LAW
    # =========================================================
    {
        "id": "it_act_sec66",
        "name": "Information Technology Act 2000 - Section 66",
        "reference": "IT Act, 2000 § 66",
        "domain": "cyber_law",
        "description": "Computer related offences. Whoever knowingly or intentionally conceals, destroys or alters any computer source code used for a computer, computer programme, computer system or computer network, when such computer source code is required to be kept or maintained by law for the time being in force, shall be punishable.",
        "relevance": "Primary provision for cyber crimes involving unauthorized computer access and data manipulation.",
        "jurisdiction": "India (Central)",
        "keywords": ["cyber crime", "computer offence", "hacking", "unauthorized access", "data tampering"],
        "sections": ["66", "66A", "66B", "66C", "66D", "66E", "66F"],
        "verified": True,
    },
    {
        "id": "it_act_sec66d",
        "name": "Information Technology Act 2000 - Section 66D",
        "reference": "IT Act, 2000 § 66D",
        "domain": "cyber_law",
        "description": "Punishment for cheating by personation by using computer resource. Whoever, by means of any communication device or computer resource cheats by personation, shall be punished with imprisonment of either description for a term which may extend to three years and shall also be liable to fine which may extend to one lakh rupees.",
        "relevance": "Core provision for online fraud, phishing, impersonation, and cyber cheating.",
        "jurisdiction": "India (Central)",
        "keywords": ["phishing", "cyber fraud", "impersonation", "online cheating", "identity fraud"],
        "sections": ["66D"],
        "verified": True,
    },
    {
        "id": "it_act_sec43",
        "name": "Information Technology Act 2000 - Section 43",
        "reference": "IT Act, 2000 § 43",
        "domain": "cyber_law",
        "description": "Penalty and compensation for damage to computer, computer system, etc. Provides civil remedy for unauthorized access to computers and networks, including downloading, introducing viruses, and disrupting service.",
        "relevance": "Civil compensation remedy for unauthorized computer access or network disruption.",
        "jurisdiction": "India (Central)",
        "keywords": ["unauthorized access", "compensation", "civil remedy", "data theft"],
        "sections": ["43", "43A"],
        "verified": True,
    },
    {
        "id": "bns_sec318",
        "name": "Bharatiya Nyaya Sanhita 2023 - Section 318",
        "reference": "BNS, 2023 § 318",
        "domain": "criminal_law",
        "description": "Cheating. Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver any property to any person, or to consent that any person shall retain any property, or intentionally induces the person so deceived to do or omit to do anything which he would not do or omit if he were not so deceived, and which act or omission causes or is likely to cause damage or harm to that person in body, mind, reputation or property, is said to 'cheat'.",
        "relevance": "General criminal provision for fraud and cheating, applicable to online fraud cases.",
        "jurisdiction": "India (Central)",
        "keywords": ["cheating", "fraud", "deception", "property", "financial fraud"],
        "sections": ["318", "319"],
        "verified": True,
    },
    {
        "id": "bns_sec316",
        "name": "Bharatiya Nyaya Sanhita 2023 - Section 316",
        "reference": "BNS, 2023 § 316",
        "domain": "criminal_law",
        "description": "Criminal breach of trust. Whoever, being in any manner entrusted with property, or with any dominion over property, dishonestly misappropriates or converts to his own use that property, or dishonestly uses or disposes of that property in violation of any direction of law prescribing the mode in which such trust is to be discharged.",
        "relevance": "Applicable in cases where trusted party misappropriates funds.",
        "jurisdiction": "India (Central)",
        "keywords": ["breach of trust", "misappropriation", "trust", "dishonest"],
        "sections": ["316"],
        "verified": True,
    },
    {
        "id": "cyber_crime_portal",
        "name": "National Cyber Crime Reporting Portal - Helpline 1930",
        "reference": "NCCRP / Cyber Crime Helpline 1930",
        "domain": "cyber_law",
        "description": "The National Cyber Crime Reporting Portal (cybercrime.gov.in) and helpline number 1930 provide mechanisms to report cyber crimes including financial fraud, social media crimes, and other online offences.",
        "relevance": "Primary reporting mechanism for cyber fraud victims in India. Must be reported within 24 hours for financial fraud freeze.",
        "jurisdiction": "India (Central)",
        "keywords": ["cyber crime reporting", "helpline", "1930", "cybercrime.gov.in", "financial fraud report"],
        "sections": [],
        "verified": True,
    },
    # =========================================================
    # CRIMINAL LAW / BAIL
    # =========================================================
    {
        "id": "bnss_sec480",
        "name": "Bharatiya Nagarik Suraksha Sanhita 2023 - Section 480",
        "reference": "BNSS, 2023 § 480",
        "domain": "criminal_law",
        "description": "Bail in bailable offences. When any person other than a person accused of a non-bailable offence is arrested or detained without warrant by an officer in charge of a police station, or appears or is brought before a Court, and is prepared at any time while in the custody of such officer or at any stage of the proceeding before such Court to give bail, such person shall be released on bail.",
        "relevance": "Governs bail in bailable offences as matter of right.",
        "jurisdiction": "India (Central)",
        "keywords": ["bail", "bailable offence", "arrest", "custody"],
        "sections": ["480"],
        "verified": True,
    },
    {
        "id": "bnss_sec483",
        "name": "Bharatiya Nagarik Suraksha Sanhita 2023 - Section 483",
        "reference": "BNSS, 2023 § 483",
        "domain": "criminal_law",
        "description": "Power of High Court and Court of Session to grant bail. The High Court or the Court of Session may direct that any person accused of an offence and in custody be released on bail and if the offence is of the nature specified in subsection (3) of section 482, may impose any condition.",
        "relevance": "Governs bail applications before Sessions Court and High Court for non-bailable offences.",
        "jurisdiction": "India (Central)",
        "keywords": ["bail", "High Court", "Sessions Court", "non-bailable", "bail application"],
        "sections": ["483"],
        "verified": True,
    },
    {
        "id": "bnss_sec482",
        "name": "Bharatiya Nagarik Suraksha Sanhita 2023 - Section 482",
        "reference": "BNSS, 2023 § 482",
        "domain": "criminal_law",
        "description": "Bail in non-bailable offence. When any person accused of, or suspected of, the commission of any non-bailable offence is arrested or detained without warrant by an officer in charge of a police station or appears or is brought before a Court other than the High Court or Court of Session, he may be released on bail.",
        "relevance": "Primary provision for bail in non-bailable offences. Key reference for bail applications.",
        "jurisdiction": "India (Central)",
        "keywords": ["bail", "non-bailable", "arrested", "custody", "bail application"],
        "sections": ["482"],
        "verified": True,
    },
    {
        "id": "bnss_anticipatory_bail",
        "name": "Bharatiya Nagarik Suraksha Sanhita 2023 - Section 484",
        "reference": "BNSS, 2023 § 484",
        "domain": "criminal_law",
        "description": "Direction for grant of bail to person apprehending arrest (Anticipatory Bail). When any person has reason to believe that he may be arrested on an accusation of having committed a non-bailable offence, he may apply to the High Court or the Court of Session for a direction that in the event of such arrest he shall be released on bail.",
        "relevance": "Anticipatory bail provision to seek pre-arrest bail protection.",
        "jurisdiction": "India (Central)",
        "keywords": ["anticipatory bail", "pre-arrest", "High Court", "Sessions Court"],
        "sections": ["484"],
        "verified": True,
    },
    # =========================================================
    # CONSUMER LAW
    # =========================================================
    {
        "id": "cpa_2019_sec2",
        "name": "Consumer Protection Act 2019 - Section 2 (Definitions)",
        "reference": "CPA, 2019 § 2",
        "domain": "consumer_law",
        "description": "Key definitions under the Consumer Protection Act 2019 including 'consumer', 'defect', 'deficiency', 'unfair trade practice', and 'service'. A consumer is any person who buys goods or avails services for consideration.",
        "relevance": "Establishes who qualifies as a consumer and what constitutes a consumer dispute.",
        "jurisdiction": "India (Central)",
        "keywords": ["consumer", "defect", "deficiency", "unfair trade", "consumer dispute"],
        "sections": ["2"],
        "verified": True,
    },
    {
        "id": "cpa_2019_sec35",
        "name": "Consumer Protection Act 2019 - Section 35",
        "reference": "CPA, 2019 § 35",
        "domain": "consumer_law",
        "description": "Complaints before District Commission. Any complainant may file a complaint before the District Consumer Disputes Redressal Commission in relation to goods with value not exceeding one crore rupees.",
        "relevance": "Filing mechanism for consumer complaints at district level. Jurisdiction up to Rs 1 crore.",
        "jurisdiction": "India (District Level)",
        "keywords": ["District Commission", "consumer complaint", "filing", "one crore"],
        "sections": ["35"],
        "verified": True,
    },
    {
        "id": "cpa_2019_sec47",
        "name": "Consumer Protection Act 2019 - Section 47",
        "reference": "CPA, 2019 § 47",
        "domain": "consumer_law",
        "description": "Jurisdiction of State Commission. The State Consumer Disputes Redressal Commission has jurisdiction to entertain complaints where value of goods or services exceeds one crore rupees but does not exceed ten crore rupees.",
        "relevance": "State Consumer Commission jurisdiction for disputes between Rs 1-10 crore.",
        "jurisdiction": "India (State Level)",
        "keywords": ["State Commission", "consumer complaint", "one crore", "ten crore"],
        "sections": ["47"],
        "verified": True,
    },
    {
        "id": "cpa_2019_sec69",
        "name": "Consumer Protection Act 2019 - Section 69",
        "reference": "CPA, 2019 § 69",
        "domain": "consumer_law",
        "description": "Limitation period. The District Commission, the State Commission or the National Commission shall not admit a complaint unless it is filed within two years from the date on which the cause of action has arisen.",
        "relevance": "2-year limitation period for filing consumer complaints.",
        "jurisdiction": "India (Central)",
        "keywords": ["limitation", "two years", "time limit", "consumer complaint"],
        "sections": ["69"],
        "verified": True,
    },
    {
        "id": "cpa_2019_remedies",
        "name": "Consumer Protection Act 2019 - Section 39 (Remedies)",
        "reference": "CPA, 2019 § 39",
        "domain": "consumer_law",
        "description": "Findings of the District Commission. Where a complaint is found to be proved, the Commission may order repair, replacement, refund, compensation for loss/injury, removal of deficiency, discontinuance of unfair trade practice, and punitive damages.",
        "relevance": "Available remedies in consumer disputes including replacement, refund, and compensation.",
        "jurisdiction": "India (Central)",
        "keywords": ["remedy", "compensation", "refund", "replacement", "repair", "deficiency"],
        "sections": ["39"],
        "verified": True,
    },
    # =========================================================
    # PROPERTY LAW
    # =========================================================
    {
        "id": "tpa_1882_sec54",
        "name": "Transfer of Property Act 1882 - Section 54",
        "reference": "TPA, 1882 § 54",
        "domain": "property_law",
        "description": "Sale defined. 'Sale' is a transfer of ownership in exchange for a price paid or promised or part-paid and part-promised. Sale of immoveable property of value one hundred rupees and upwards can be made only by a registered instrument.",
        "relevance": "Defines valid property sale and registration requirement for immovable property.",
        "jurisdiction": "India (Central)",
        "keywords": ["sale", "property transfer", "registered", "immovable property", "ownership"],
        "sections": ["54"],
        "verified": True,
    },
    {
        "id": "tpa_1882_sec58",
        "name": "Transfer of Property Act 1882 - Section 58",
        "reference": "TPA, 1882 § 58",
        "domain": "property_law",
        "description": "Mortgage defined. A mortgage is the transfer of an interest in specific immoveable property for the purpose of securing the payment of money advanced or to be advanced by way of loan.",
        "relevance": "Defines mortgages on property, relevant in property disputes involving encumbrances.",
        "jurisdiction": "India (Central)",
        "keywords": ["mortgage", "encumbrance", "property", "loan", "immovable property"],
        "sections": ["58"],
        "verified": True,
    },
    {
        "id": "specific_relief_act_sec6",
        "name": "Specific Relief Act 1963 - Section 6",
        "reference": "SRA, 1963 § 6",
        "domain": "property_law",
        "description": "Suit by person dispossessed of immovable property. If any person is dispossessed without his consent of immovable property otherwise than in due course of law, he or any person through whom he claims may, by suit, recover possession thereof, notwithstanding any other title that may be set up in such suit.",
        "relevance": "Remedy for wrongful dispossession of property regardless of title disputes.",
        "jurisdiction": "India (Central)",
        "keywords": ["dispossession", "possession", "property", "recovery", "civil suit"],
        "sections": ["6"],
        "verified": True,
    },
    {
        "id": "specific_relief_act_sec34",
        "name": "Specific Relief Act 1963 - Section 34",
        "reference": "SRA, 1963 § 34",
        "domain": "property_law",
        "description": "Discretion of court as to declaration of status or right. Any person entitled to any legal character, or to any right as to any property, may institute a suit against any person denying, or interested to deny, his title to such character or right.",
        "relevance": "Declaration of title suits for property ownership disputes.",
        "jurisdiction": "India (Central)",
        "keywords": ["declaration of title", "property rights", "title suit", "ownership"],
        "sections": ["34"],
        "verified": True,
    },
    {
        "id": "registration_act_1908",
        "name": "Registration Act 1908",
        "reference": "Registration Act, 1908",
        "domain": "property_law",
        "description": "Governs registration of documents relating to property transactions. Section 17 mandates registration of instruments related to immovable property of value Rs 100 or more. Unregistered documents cannot be used as evidence for the transaction.",
        "relevance": "Mandatory registration of property sale deeds; unregistered documents have limited evidentiary value.",
        "jurisdiction": "India (Central)",
        "keywords": ["registration", "property", "sale deed", "immovable", "document"],
        "sections": ["17", "49"],
        "verified": True,
    },
    {
        "id": "limitation_act_sec3",
        "name": "Limitation Act 1963 - Section 3",
        "reference": "Limitation Act, 1963 § 3",
        "domain": "civil_law",
        "description": "Bar of limitation. Subject to the provisions contained in sections 4 to 24, every suit instituted, appeal preferred, and application made after the prescribed period shall be dismissed.",
        "relevance": "Governs time limits for filing civil suits. Property suits generally have 3 or 12-year limits.",
        "jurisdiction": "India (Central)",
        "keywords": ["limitation period", "time limit", "civil suit", "prescription"],
        "sections": ["3"],
        "verified": True,
    },
]


class LegalKnowledgeBase:
    """
    Verified Indian Legal Knowledge Base.
    Provides lookup by ID, reference string, domain, and keyword.
    """

    def __init__(self):
        self._laws: Dict[str, LawReference] = {}
        self._by_domain: Dict[str, List[LawReference]] = {}
        self._load()

    def _load(self):
        for entry in _LAWS:
            law = LawReference(**entry)
            self._laws[law.id] = law
            domain = law.domain
            if domain not in self._by_domain:
                self._by_domain[domain] = []
            self._by_domain[domain].append(law)

    def get_law_by_id(self, law_id: str) -> Optional[LawReference]:
        """Get a law by its canonical ID."""
        return self._laws.get(law_id)

    def find_law_by_reference(self, reference: str) -> Optional[LawReference]:
        """Find a law by matching reference string or name (case-insensitive)."""
        ref_lower = reference.lower()
        for law in self._laws.values():
            if (
                ref_lower in law.reference.lower()
                or ref_lower in law.name.lower()
                or law.id.lower() == ref_lower
            ):
                return law
        return None

    def get_laws_by_domain(self, domain: str) -> List[LawReference]:
        """Get all laws for a given domain."""
        return self._by_domain.get(domain, [])

    def search_laws(self, query: str) -> List[LawReference]:
        """Full-text keyword search across all laws."""
        query_lower = query.lower()
        results = []
        for law in self._laws.values():
            score = 0
            if query_lower in law.name.lower():
                score += 3
            if query_lower in law.description.lower():
                score += 2
            if any(query_lower in kw.lower() for kw in law.keywords):
                score += 2
            if query_lower in law.reference.lower():
                score += 1
            if score > 0:
                results.append((score, law))
        results.sort(key=lambda x: x[0], reverse=True)
        return [law for _, law in results]

    def get_all_laws(self) -> List[LawReference]:
        """Return all laws in the knowledge base."""
        return list(self._laws.values())

    def get_all_domains(self) -> List[str]:
        """Return all domains present in the knowledge base."""
        return list(self._by_domain.keys())

    def law_exists(self, law_id: str) -> bool:
        return law_id in self._laws
