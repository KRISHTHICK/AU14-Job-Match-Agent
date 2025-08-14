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
