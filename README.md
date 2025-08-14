# AU14-Job-Match-Agent
Ai Agent

What it does:

Upload your resume (PDF)

Paste a job description (or upload a text file)

Agent extracts skills & keywords, measures fit score, highlights gaps, suggests improvements, and (optionally) drafts a cover letter.

Works fully offline using spaCy + regex + TF-IDF. If you add an OpenAI key, it upgrades the copywriting.

After installing, download a small spaCy model:

python -m spacy download en_core_web_sm

In .env folder
If you leave PROVIDER=none, the app still works (it uses a solid local template).

**************************************

📘 README.md
# Job-Match Agent

Upload your resume (PDF) + paste a JD → get:
- Fit score
- Keyword overlap & gaps
- Actionable suggestions
- A draft cover letter (local template or OpenAI, if configured)

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cp .env.example .env          # optional: set OPENAI_API_KEY
streamlit run app.py

How it works

Parse: Extract text from PDF (PyMuPDF) and clean it.

Mine keywords:

spaCy noun chunks + POS highlights

TF-IDF on resume vs JD (bigrams too)

Skill buckets: lightweight tech/soft dictionaries.

Score: overlap / JD requested terms.

Coach: gap-based suggestions.

Cover letter:

If OpenAI configured: LLM prompt

Else: strong local template

Notes

No network required unless you opt into OpenAI for copywriting.

The dictionary lists in utils/nlp.py are easy to extend per role/domain.


---

## 🧹 .gitignore

```gitignore
.venv/
__pycache__/
.DS_Store
.env
.streamlit/

▶️ Run
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py

Why this agent?

Useful immediately (resume + JD = insights you can act on today).

Offline-first (no key required).

LLM-upgradeable (nicer letters if you add OpenAI).

Extensible (plug in your own skill dictionaries or add a company-specific template).
