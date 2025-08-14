import re
import spacy
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

# Load once
try:
    NLP = spacy.load("en_core_web_sm")
except OSError:
    # Friendly error if the user forgot to download the model
    raise SystemExit("spaCy model missing. Run: python -m spacy download en_core_web_sm")

TECH_TERMS = set(x.lower() for x in """
python java javascript typescript go rust c c++ c# sql nosql postgresql mysql mongo
aws gcp azure docker kubernetes terraform airflow spark hadoop databricks kafka
pytorch tensorflow scikit-learn spaCy huggingface langchain mlflow opencv
react vue angular django flask fastapi node express spring .net nextjs
graphql rest grpc microservices serverless linux unix bash powershell git ci/cd
pytest junit playwright cypress selenium jira confluence tableau powerbi
nlp nlu nlg llm rag vector embeddings pinecone weaviate chroma qdrant
""".split())

SOFT_TERMS = set(x.lower() for x in """
leadership communication collaboration stakeholder mentoring ownership autonomy initiative
problem-solving critical-thinking adaptability creativity time-management
""".split())

def clean_text(t: str) -> str:
    t = re.sub(r"[^\x09\x0A\x0D\x20-\x7E]", " ", t)   # strip weird unicode
    t = re.sub(r"\s+", " ", t).strip()
    return t

def keyphrases_spacy(text: str, top_k=25):
    doc = NLP(text)
    # collect NPs and PROPN/VERB/ADJ sequences
    cands = []
    for chunk in doc.noun_chunks:
        if 2 <= len(chunk.text) <= 60:
            cands.append(chunk.lemma_.lower())
    cands.extend([t.lemma_.lower() for t in doc if t.pos_ in {"PROPN","VERB","ADJ"} and len(t) > 2])
    counts = Counter(cands)
    return [w for w,_ in counts.most_common(top_k)]

def tfidf_keywords(corpus: list[str], top_k=30):
    vec = TfidfVectorizer(ngram_range=(1,2), max_features=4000, stop_words="english")
    X = vec.fit_transform(corpus)
    vocab = vec.get_feature_names_out()
    # take top by tfidf in the JD (assume index 1 = JD)
    jd_vec = X[1].toarray().ravel()
    idxs = jd_vec.argsort()[::-1][:top_k]
    return [vocab[i] for i in idxs if len(vocab[i]) > 2]

def extract_skills(text: str):
    words = set(re.findall(r"[A-Za-z][A-Za-z\+\#\.\-/0-9]*", text.lower()))
    tech = sorted(words & TECH_TERMS)
    soft = sorted(words & SOFT_TERMS)
    return tech, soft

def compute_fit_score(resume_terms: set[str], jd_terms: set[str]) -> float:
    if not jd_terms: return 0.0
    hit = len(resume_terms & jd_terms)
    return round(100.0 * hit / len(jd_terms), 1)
