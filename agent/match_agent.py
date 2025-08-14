from dataclasses import dataclass
from utils.pdf_text.py import extract_text_from_pdf  # import fix below!
from utils.nlp import clean_text, keyphrases_spacy, tfidf_keywords, extract_skills, compute_fit_score
from utils.cover_letter import render_cover_letter_fallback
from utils.llm import maybe_generate_cover_letter

# NOTE: Python import path fix — correct import:
from utils.pdf_text import extract_text_from_pdf  # <-- use this one

@dataclass
class MatchResult:
    resume_text: str
    jd_text: str
    resume_keywords: list[str]
    jd_keywords: list[str]
    overlap_keywords: list[str]
    missing_keywords: list[str]
    tech_resume: list[str]
    soft_resume: list[str]
    tech_jd: list[str]
    soft_jd: list[str]
    fit_score: float
    suggestions: list[str]
    cover_letter: str

def suggest_improvements(missing_keywords, jd_text):
    sugg = []
    if missing_keywords:
        top_miss = ", ".join(missing_keywords[:8])
        sugg.append(f"Consider adding evidence of: {top_miss}.")
    if "lead" in jd_text.lower():
        sugg.append("Add leadership examples: team size, scope, decisions, outcomes.")
    if "communication" in jd_text.lower():
        sugg.append("Show cross-functional collaboration and stakeholder comms outcomes.")
    if "cloud" in jd_text.lower():
        sugg.append("Mention specific cloud services used (e.g., AWS Lambda, S3, IAM).")
    if "data" in jd_text.lower():
        sugg.append("Quantify data scale (rows, GB, throughput) and performance gains.")
    return sugg

def build_cover_letter(candidate_name, role, company, jd_text, resume_text, overlap, missing):
    llm_prompt = f"""
Write a crisp, 250–350 word cover letter for {candidate_name} applying to {company} as {role}.
Use resume highlights:
{resume_text[:1200]}

Align to JD (focus areas):
{jd_text[:1000]}

Emphasize strengths seen in overlap keywords: {", ".join(overlap[:12])}
Acknowledge growth areas (1 line): {", ".join(missing[:6])}
Tone: confident, specific, human. No clichés, no fluff, no generic promises.
"""
    drafted = maybe_generate_cover_letter(llm_prompt)
    if drafted:
        return drafted
    # Fallback (local template)
    return render_cover_letter_fallback(
        company=company or "Company",
        company_location="",
        role=role or "Role",
        years_exp="5",
        domains="data platforms, ML, and backend systems",
        bullets="- Built ETL platform that cut costs 30%\n- Productionized ML models serving 50M req/day\n- Led 6-engineer team to ship features faster by 40%",
        strengths=", ".join(overlap[:6]) or "problem solving, ownership, delivery",
        gaps_to_close=", ".join(missing[:3]) or "few items",
        teams="Product & Engineering",
        company_short=company or "the team",
        candidate=candidate_name or "Your Name",
        contact="email • phone • LinkedIn",
    )

def analyze_match(resume_text: str, jd_text: str, candidate_name=""):
    rtext = clean_text(resume_text)
    jtext = clean_text(jd_text)

    # keyword mining
    r_kps = keyphrases_spacy(rtext, top_k=40)
    j_kps = keyphrases_spacy(jtext, top_k=40)
    tfidf = tfidf_keywords([rtext, jtext], top_k=30)
    jd_keywords = list(dict.fromkeys((j_kps + tfidf)))  # uniq while preserving order

    # skills buckets
    r_tech, r_soft = extract_skills(rtext)
    j_tech, j_soft = extract_skills(jtext)

    resume_terms = set(r_kps + r_tech + r_soft)
    jd_terms = set(jd_keywords + j_tech + j_soft)

    overlap = sorted(resume_terms & jd_terms)
    missing = sorted(jd_terms - resume_terms)

    score = compute_fit_score(resume_terms, jd_terms)

    suggestions = suggest_improvements(missing, jtext)

    cover_letter = build_cover_letter(candidate_name, role="", company="", jd_text=jtext,
                                      resume_text=rtext, overlap=overlap, missing=missing)

    return MatchResult(
        resume_text=rtext,
        jd_text=jtext,
        resume_keywords=sorted(set(r_kps)),
        jd_keywords=jd_keywords,
        overlap_keywords=overlap,
        missing_keywords=missing,
        tech_resume=r_tech, soft_resume=r_soft,
        tech_jd=j_tech, soft_jd=j_soft,
        fit_score=score,
        suggestions=suggestions,
        cover_letter=cover_letter
    )
