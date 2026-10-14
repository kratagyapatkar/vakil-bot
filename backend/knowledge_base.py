"""
Legal Knowledge Base Builder
Scrapes and loads publicly available Indian legal information:
- Constitution of India (key articles)
- IPC / BNS sections
- CPC sections
- Consumer Protection Act
- RTI Act
- IndianKanoon public API
"""

import json
import os
from typing import List
from langchain_core.documents import Document


# ─── Static Legal Knowledge ──────────────────────────────────────────────────

INDIAN_LEGAL_KNOWLEDGE = [
    # ── CONSTITUTION ──────────────────────────────────────────────
    {
        "text": "Article 14 of the Constitution of India: The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India. This is a fundamental right enforceable under Article 32 (Supreme Court) and Article 226 (High Court).",
        "source": "Constitution of India - Article 14",
        "category": "Fundamental Rights",
        "tags": ["equality", "discrimination", "fundamental rights"]
    },
    {
        "text": "Article 19 of the Constitution of India guarantees six fundamental freedoms: (a) freedom of speech and expression, (b) freedom to assemble peaceably, (c) freedom to form associations, (d) freedom to move freely throughout India, (e) freedom to reside and settle in any part of India, (g) freedom to practice any profession or trade. These rights are subject to reasonable restrictions by the State.",
        "source": "Constitution of India - Article 19",
        "category": "Fundamental Rights",
        "tags": ["freedom of speech", "fundamental rights", "freedom of movement"]
    },
    {
        "text": "Article 21 of the Constitution of India: No person shall be deprived of his life or personal liberty except according to procedure established by law. The Supreme Court has expanded this to include rights to livelihood, privacy, health, education, and a dignified life. Violation can be challenged via Habeas Corpus (Article 32/226).",
        "source": "Constitution of India - Article 21",
        "category": "Fundamental Rights",
        "tags": ["right to life", "personal liberty", "privacy", "habeas corpus"]
    },
    {
        "text": "Article 22 of the Constitution: A person who is arrested must be informed of the grounds of arrest, be allowed to consult a lawyer of their choice, and must be produced before the nearest Magistrate within 24 hours of arrest (excluding travel time). Preventive detention laws are governed by Article 22(4)-(7).",
        "source": "Constitution of India - Article 22",
        "category": "Fundamental Rights",
        "tags": ["arrest", "detention", "rights of arrested person", "magistrate", "24 hours"]
    },
    {
        "text": "Article 32 of the Constitution gives citizens the right to approach the Supreme Court directly for enforcement of Fundamental Rights. Writs available: Habeas Corpus (release from illegal detention), Mandamus (compel authority to perform duty), Prohibition (stop lower court from exceeding jurisdiction), Certiorari (quash lower court order), Quo Warranto (challenge person's right to hold public office).",
        "source": "Constitution of India - Article 32",
        "category": "Constitutional Remedies",
        "tags": ["writ petition", "supreme court", "habeas corpus", "mandamus", "certiorari"]
    },
    {
        "text": "Article 39A of the Constitution mandates free legal aid to the poor. This is implemented through the Legal Services Authorities Act, 1987. The National Legal Services Authority (NALSA) provides free legal services to women, SC/ST, persons with disabilities, industrial workmen, persons in custody, victims of mass disaster, and persons with annual income below Rs. 3 lakh (for High Courts) or Rs. 5 lakh (for Supreme Court).",
        "source": "Constitution of India - Article 39A & NALSA",
        "category": "Legal Aid",
        "tags": ["free legal aid", "NALSA", "legal services", "poor", "SC/ST", "women"]
    },

    # ── IPC / BNS ──────────────────────────────────────────────────
    {
        "text": "Bharatiya Nyaya Sanhita (BNS) 2023 has replaced the Indian Penal Code (IPC) 1860 with effect from 1 July 2024. BNS Section 103 (Murder, equivalent to IPC 302) — Punishment: Death or imprisonment for life, and fine. BNS Section 105 (Culpable Homicide Not Amounting to Murder, equivalent to IPC 304) — Punishment: Up to life imprisonment or up to 10 years + fine.",
        "source": "Bharatiya Nyaya Sanhita 2023 - Sections 103, 105",
        "category": "Criminal Law",
        "tags": ["murder", "homicide", "BNS", "IPC 302", "death penalty"]
    },
    {
        "text": "BNS Section 64 (Rape, equivalent to IPC 376): Punishment — not less than 10 years rigorous imprisonment, which may extend to life imprisonment, and fine. Rape of a woman under 12 years: minimum 20 years, may extend to life or death. A woman cannot be arrested after sunset and before sunrise without Magistrate's permission. Medical examination of rape survivor must be done within 24 hours of report.",
        "source": "Bharatiya Nyaya Sanhita 2023 - Section 64",
        "category": "Criminal Law",
        "tags": ["rape", "sexual assault", "IPC 376", "POCSO", "women safety"]
    },
    {
        "text": "BNS Section 303 (Theft, equivalent to IPC 378): Whoever, intending to take dishonestly any moveable property out of the possession of any person without that person's consent, commits theft. Punishment under BNS 305: up to 3 years imprisonment, or fine, or both. Repeat offenders face enhanced punishment.",
        "source": "Bharatiya Nyaya Sanhita 2023 - Sections 303, 305",
        "category": "Criminal Law",
        "tags": ["theft", "property crime", "IPC 378", "moveable property"]
    },
    {
        "text": "BNS Section 316 (Cheating, equivalent to IPC 420): Whoever cheats and thereby dishonestly induces the person deceived to deliver any property, or to make, alter or destroy a valuable security, commits cheating. Punishment: up to 7 years imprisonment and fine. Online cheating/fraud is also covered under IT Act Section 66C and 66D.",
        "source": "Bharatiya Nyaya Sanhita 2023 - Section 316 & IT Act",
        "category": "Criminal Law",
        "tags": ["cheating", "fraud", "IPC 420", "online fraud", "cybercrime"]
    },
    {
        "text": "BNS Section 352 (Defamation, equivalent to IPC 499-500): Making or publishing any imputation concerning a person intending to harm reputation. Exceptions include truth for public good, fair criticism of public conduct, reports of court proceedings. Punishment: up to 2 years simple imprisonment, or fine, or both. Civil defamation (tort) can also be pursued in civil courts for damages.",
        "source": "Bharatiya Nyaya Sanhita 2023 - Section 352",
        "category": "Criminal Law",
        "tags": ["defamation", "reputation", "IPC 499", "slander", "libel"]
    },
    {
        "text": "Domestic Violence — The Protection of Women from Domestic Violence Act, 2005 (PWDVA) covers physical, sexual, verbal, emotional, and economic abuse. The aggrieved woman can approach a Protection Officer or Magistrate for: Protection Orders, Residence Orders, Monetary Relief, Custody Orders, and Compensation Orders. The complaint can be filed at the police station or directly in Magistrate's court.",
        "source": "Protection of Women from Domestic Violence Act, 2005",
        "category": "Family Law",
        "tags": ["domestic violence", "DV Act", "women protection", "protection order", "PWDVA"]
    },

    # ── CONSUMER LAW ──────────────────────────────────────────────
    {
        "text": "Consumer Protection Act 2019: A consumer can file a complaint against defective goods, deficient services, unfair trade practices, and overcharging. Forums: District Commission (claims up to Rs. 1 crore), State Commission (Rs. 1 crore to Rs. 10 crore), National Commission (above Rs. 10 crore). Complaint can also be filed online at edaakhil.nic.in. Limitation: within 2 years of cause of action.",
        "source": "Consumer Protection Act, 2019",
        "category": "Consumer Law",
        "tags": ["consumer complaint", "defective product", "consumer forum", "edaakhil", "refund"]
    },
    {
        "text": "E-commerce complaints under Consumer Protection (E-Commerce) Rules 2020: E-commerce entities must have a Grievance Officer with contact details displayed on their website. Complaints must be acknowledged within 48 hours and resolved within 1 month. If unresolved, consumers can file at edaakhil.nic.in or approach the District Consumer Commission.",
        "source": "Consumer Protection (E-Commerce) Rules 2020",
        "category": "Consumer Law",
        "tags": ["ecommerce", "online shopping", "amazon flipkart", "refund", "consumer rights"]
    },

    # ── RTI ────────────────────────────────────────────────────────
    {
        "text": "Right to Information Act 2005 (RTI): Any citizen can request information from public authorities. Submit application to the Public Information Officer (PIO) with Rs. 10 fee (BPL families exempt). The authority must respond within 30 days (48 hours for life/liberty matters). First Appeal: to appellate officer within 30 days of PIO response. Second Appeal/Complaint: to Central/State Information Commission within 90 days. Penalty for PIO delay: Rs. 250/day up to Rs. 25,000.",
        "source": "Right to Information Act, 2005",
        "category": "RTI",
        "tags": ["RTI", "right to information", "government information", "PIO", "transparency"]
    },

    # ── LABOUR LAW ────────────────────────────────────────────────
    {
        "text": "Labour Laws — Key protections: (1) Minimum Wages Act ensures minimum wage payment. (2) Payment of Wages Act requires timely wage payment. (3) Maternity Benefit Act provides 26 weeks paid maternity leave. (4) POSH Act (Sexual Harassment at Workplace) requires Internal Complaints Committee in organizations with 10+ employees. (5) Gratuity is mandatory after 5 years of continuous service. Complaints can be filed with the Labour Commissioner.",
        "source": "Indian Labour Laws - Consolidated",
        "category": "Labour Law",
        "tags": ["wages", "maternity leave", "sexual harassment", "workplace", "gratuity", "labour"]
    },
    {
        "text": "Prevention, Prohibition and Redressal of Sexual Harassment at Workplace Act (POSH) 2013: Every employer with 10+ employees must constitute an Internal Complaints Committee (ICC). Complaint must be filed within 3 months of incident. ICC must complete inquiry within 60 days. If no ICC, complaint goes to Local Complaints Committee (LCC) at district level. Employer can face fine up to Rs. 50,000 for non-compliance.",
        "source": "POSH Act, 2013",
        "category": "Labour Law",
        "tags": ["sexual harassment", "workplace", "POSH", "ICC", "women safety", "employer"]
    },

    # ── PROPERTY LAW ──────────────────────────────────────────────
    {
        "text": "Property Disputes — Key laws: (1) Transfer of Property Act 1882 governs sale, mortgage, lease, gift of property. (2) Registration Act 1908 — property documents above Rs. 100 must be registered. (3) Limitation Act — suit for recovery of immoveable property must be filed within 12 years. (4) Land Acquisition — fair compensation must be paid under Right to Fair Compensation and Transparency in Land Acquisition Act 2013 (minimum 4x market value for rural land).",
        "source": "Transfer of Property Act 1882 & Related Laws",
        "category": "Property Law",
        "tags": ["property", "land", "registration", "sale deed", "mortgage", "land acquisition"]
    },
    {
        "text": "Tenant Rights under Rent Control Acts (varies by state): Tenants cannot be evicted without court order. Landlord must provide rent receipt. Rent Agreement should be registered if period exceeds 11 months. Security deposit refund must be made after vacating. In Delhi, Maharashtra, and other states, specific Rent Control Acts protect tenants from arbitrary eviction and unreasonable rent increases.",
        "source": "State Rent Control Acts (Delhi, Maharashtra, etc.)",
        "category": "Property Law",
        "tags": ["tenant", "rent", "eviction", "landlord", "rent agreement", "security deposit"]
    },

    # ── CYBER LAW ─────────────────────────────────────────────────
    {
        "text": "Information Technology Act 2000 (IT Act) — Key sections: Section 66A (struck down by SC), Section 66C (identity theft — 3 years + fine), Section 66D (cheating by impersonation using computer — 3 years + fine), Section 67 (publishing obscene material — 3 years + fine for first conviction), Section 69 (government power to intercept/decrypt data). Cybercrime complaints: cybercrime.gov.in (National Cybercrime Reporting Portal).",
        "source": "Information Technology Act, 2000",
        "category": "Cyber Law",
        "tags": ["cybercrime", "hacking", "IT Act", "identity theft", "online fraud", "cybercrime.gov.in"]
    },
    {
        "text": "Cybercrime Reporting in India: Report at cybercrime.gov.in or call 1930 (National Cybercrime Helpline). For financial fraud (UPI, online banking), report immediately to your bank and at 1930 to freeze the money. Types of cybercrime: phishing, online fraud, cyberstalking, morphed images, ransomware, social media hacking. Jurisdiction lies where victim resides or where crime originated.",
        "source": "Ministry of Home Affairs - Cybercrime Portal",
        "category": "Cyber Law",
        "tags": ["cybercrime helpline", "1930", "online fraud", "phishing", "cyberstalking", "report"]
    },

    # ── FAMILY LAW ────────────────────────────────────────────────
    {
        "text": "Divorce in India — Hindu Marriage Act 1955: Grounds for divorce include cruelty, adultery, desertion (2 years), conversion to another religion, mental disorder, communicable disease, renunciation of world, or presumed death. Mutual consent divorce: 6-month cooling period (can be waived by courts as per 2023 SC judgment). Maintenance can be claimed by either spouse under Section 25 HMA or Section 125 CrPC (BNSS Section 144).",
        "source": "Hindu Marriage Act, 1955",
        "category": "Family Law",
        "tags": ["divorce", "Hindu marriage", "maintenance", "alimony", "mutual consent", "cruelty"]
    },
    {
        "text": "Child Custody in India: Courts decide custody based on 'best interest of the child'. Factors: child's age, education, health, parental capacity, child's preference (if older). Types: Physical custody (day-to-day care) and Legal custody (decision-making). Grandparents can also petition for visitation. International child abduction is dealt under The Hague Convention (India is not a signatory but MHA has guidelines).",
        "source": "Guardians and Wards Act, 1890 & Hindu Minority and Guardianship Act, 1956",
        "category": "Family Law",
        "tags": ["child custody", "guardianship", "divorce", "best interest of child", "visitation"]
    },

    # ── BANKING / FINANCIAL ───────────────────────────────────────
    {
        "text": "Banking Complaints: First contact bank's Grievance Redressal Officer. If unresolved in 30 days, file with Banking Ombudsman (now Integrated Ombudsman Scheme, RBI). Online: cms.rbi.org.in. Covers: failure to honour cheques, delay in credit, fraudulent transactions, UPI issues. Insurance complaints: Bima Bharosa Portal or Insurance Ombudsman. SEBI complaints (stocks): scores.gov.in.",
        "source": "RBI - Integrated Ombudsman Scheme 2021",
        "category": "Banking & Finance",
        "tags": ["banking complaint", "ombudsman", "RBI", "UPI fraud", "insurance", "SEBI", "cms.rbi.org.in"]
    },

    # ── HOW TO FILE COMPLAINT / GENERAL PROCESS ───────────────────
    {
        "text": "How to file an FIR (First Information Report) in India: Go to the nearest police station (any station for cognizable offences under BNSS Section 173). Police CANNOT refuse to register FIR for cognizable offences. If police refuses: (1) Send complaint by post to Superintendent of Police, (2) File complaint before Magistrate under BNSS Section 175(3), (3) File complaint on the state police portal. FIR copy must be given to complainant free of cost.",
        "source": "Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023 - Section 173",
        "category": "Criminal Procedure",
        "tags": ["FIR", "police", "complaint", "cognizable offence", "right to FIR", "magistrate"]
    },
    {
        "text": "Bail in India under BNSS 2023: Bailable offences — bail is a right, granted by police or court. Non-bailable offences — bail is discretionary, granted only by court. Bail factors: nature of offence, likelihood of fleeing, past record, community ties. Anticipatory Bail (BNSS Section 482): applied to Session Court or High Court before arrest. Supreme Court has held bail is the rule, jail is the exception.",
        "source": "Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023",
        "category": "Criminal Procedure",
        "tags": ["bail", "anticipatory bail", "non-bailable", "bailable", "BNSS", "arrest"]
    },
    {
        "text": "Legal Aid in India — How to get free legal help: Contact NALSA (National Legal Services Authority) at nalsa.gov.in or call 15100. District Legal Services Authority (DLSA) in every district provides free lawyers. Eligible: women, SC/ST, children, persons with disability, industrial workmen, persons in custody, victims of trafficking, and persons below income threshold. Lok Adalat: Alternative dispute resolution — awards are final and binding, no court fee.",
        "source": "Legal Services Authorities Act, 1987 & NALSA",
        "category": "Legal Aid",
        "tags": ["free legal aid", "NALSA", "Lok Adalat", "DLSA", "lawyer", "legal help", "15100"]
    },
    {
        "text": "National Important Helplines in India: Police — 100, Fire — 101, Ambulance — 102, Women Helpline — 1091, Child Helpline — 1098, Senior Citizen Helpline — 14567, Cybercrime — 1930, National Legal Services — 15100, Consumer Helpline — 1800-11-4000, Mental Health — iCall: 9152987821, Anti-Corruption (CVC) — 1800-11-0180.",
        "source": "Government of India - Emergency Helplines",
        "category": "Emergency Contacts",
        "tags": ["helpline", "emergency", "police", "women helpline", "child helpline", "contact"]
    },
    {
        "text": "POCSO Act 2012 (Protection of Children from Sexual Offences): Protects children (under 18) from sexual abuse, harassment, and exploitation. All offences under POCSO are cognizable and non-bailable. FIR must be registered by police immediately. Special Courts handle POCSO cases. Trial must be completed within 1 year. Child's identity cannot be disclosed. Medical examination must be done by female doctor for girl child. Mandatory reporting: any person aware of POCSO offence must report to police or SJPU.",
        "source": "Protection of Children from Sexual Offences Act, 2012",
        "category": "Child Protection",
        "tags": ["POCSO", "child abuse", "sexual offence", "minor", "child protection", "special court"]
    },
]


def build_documents() -> List[Document]:
    """Convert legal knowledge base into LangChain Documents."""
    documents = []
    for item in INDIAN_LEGAL_KNOWLEDGE:
        doc = Document(
            page_content=item["text"],
            metadata={
                "source": item["source"],
                "category": item["category"],
                "tags": ", ".join(item["tags"])
            }
        )
        documents.append(doc)
    return documents


if __name__ == "__main__":
    docs = build_documents()
    print(f"✅ Loaded {len(docs)} legal knowledge documents")
    for doc in docs[:3]:
        print(f"\n📚 {doc.metadata['source']}")
        print(f"   {doc.page_content[:100]}...")
