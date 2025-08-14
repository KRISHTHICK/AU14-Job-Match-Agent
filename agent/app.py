import os
import io
import streamlit as st
from dotenv import load_dotenv
from agent.match_agent import analyze_match
from utils.pdf_text import extract_text_from_pdf

load_dotenv()
st.set_page_config(page_title="Job-Match Agent", layout="wide")
st.title("🧑‍💼 Job-Match Agent")

st.caption("Upload your resume (PDF) and paste a job description. The agent scores fit, shows gaps, and drafts a cover letter.")

colL, colR = st.columns(2, gap="large")

with colL:
    resume_file = st.file_uploader("Resume (PDF)", type=["pdf"])
    resume_text_area = st.text_area("…or paste resume text", height=200, placeholder="If no PDF, paste plain text resume here")
    candidate_name = st.text_input("Your name (for cover letter)", value="Your Name")

with colR:
    jd_text_area = st.text_area("Job Description (paste text)", height=360, placeholder="Paste the JD here…")

run = st.button("Analyze Match", type="primary", use_container_width=True)

if run:
    if not (resume_file or resume_text_area.strip()):
        st.error("Please upload a resume PDF or paste resume text.")
        st.stop()
    if not jd_text_area.strip():
        st.error("Please paste a job description.")
        st.stop()

    if resume_file:
        resume_bytes = resume_file.read()
        resume_text = extract_text_from_pdf(resume_bytes)
    else:
        resume_text = resume_text_area

    with st.spinner("Scoring and drafting…"):
        result = analyze_match(resume_text, jd_text_area, candidate_name=candidate_name)

    st.success(f"Fit Score: {result.fit_score}%")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Overlap keywords", len(result.overlap_keywords))
    with c2: st.metric("Missing keywords", len(result.missing_keywords))
    with c3: st.metric("Tech skills matched", len(set(result.tech_resume) & set(result.tech_jd)))

    st.subheader("Overlap (You already cover)")
    st.write(", ".join(result.overlap_keywords[:80]) or "—")

    st.subheader("Gaps (Worth addressing)")
    st.write(", ".join(result.missing_keywords[:80]) or "—")

    st.subheader("Resume Skills (detected)")
    st.write("**Tech:**", ", ".join(result.tech_resume) or "—")
    st.write("**Soft:**", ", ".join(result.soft_resume) or "—")

    st.subheader("JD Skills (detected)")
    st.write("**Tech:**", ", ".join(result.tech_jd) or "—")
    st.write("**Soft:**", ", ".join(result.soft_jd) or "—")

    st.subheader("Suggestions to Improve Your Resume")
    for s in result.suggestions:
        st.markdown(f"- {s}")

    st.subheader("Draft Cover Letter")
    st.text_area("You can copy-edit here:", value=result.cover_letter, height=320)

    txt = io.BytesIO(result.cover_letter.encode("utf-8"))
    st.download_button("⬇️ Download Cover Letter (TXT)", data=txt, file_name="cover_letter.txt", mime="text/plain")

else:
    st.info("Tip: higher quality cover letters if you set `PROVIDER=openai` and add `OPENAI_API_KEY` in `.env`. The rest works offline.")
