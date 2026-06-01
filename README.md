# ✚ MedChat — Trusted Medical Information Chatbot

A RAG-powered medical chatbot that answers health questions using **only verified clinical sources** — NIH, CDC, WHO, Mayo Clinic, PubMed, NHS, peer-reviewed journals, and more. Unrecognised domains are rejected before scraping. Low-confidence answers are flagged explicitly rather than guessing.

```
User Message
     ↓
Question Analysis
     ↓
Trusted Medical Web Search
  (allowlist: NIH, CDC, WHO, Mayo, PubMed, NHS…)
     ↓
Web Scraping (trusted domains only)
     ↓
Text Cleaning
     ↓
Chunking
     ↓
Vector Database (ChromaDB / Pinecone)
     ↓
Semantic Retrieval + Confidence Scoring
     ↓
OpenAI GPT-4o
  (grounded system prompt + low-confidence detection)
     ↓
Final Answer  ← "I don't know" when confidence is low
```

---

## 🛡 Safety design

| Feature | Detail |
|---|---|
| **Domain allowlist** | Only 25+ pre-approved medical domains are ever scraped |
| **Confidence threshold** | Answers below cosine similarity threshold are flagged low-confidence |
| **"I don't know" fallback** | LLM instructed to say it doesn't know rather than guess |
| **Disclaimer on every answer** | Standard ⚕ disclaimer appended to all medical responses |
| **Emergency notice** | Input bar shows "call emergency services" note |
| **No memory of prior sessions** | Each session is isolated; no PII stored |

### Trusted domains (allowlist)

NIH, PubMed, MedlinePlus, CDC, WHO, Mayo Clinic, Cleveland Clinic,
Johns Hopkins Medicine, WebMD, Healthline, Medical News Today, BMJ,
The Lancet, NEJM, JAMA, ACP Journals, UpToDate, Medscape, Merck Manuals,
Drugs.com, RxList, FDA, NHS, NICE.

---

## 🚀 Quickstart

```bash
git clone https://github.com/kitescripter/medchat.git
cd medchat
cp .env.example .env   # add your keys
cd backend && pip install -r requirements.txt
uvicorn api.main:app --reload
# in another terminal:
cd frontend && npm install && npm run dev
```

Visit `http://localhost:5173`

---

## 🗂 Project Structure

```
medchat/
├── backend/
│   ├── api/main.py                  # FastAPI /chat endpoint
│   ├── config.py                    # Trusted domains allowlist + confidence config
│   ├── pipeline/
│   │   ├── question_analysis.py     # Intent + keyword extraction
│   │   ├── search.py                # Web search → trusted-domain filter
│   │   ├── chunker.py               # Recursive text chunker
│   │   ├── embedder.py              # OpenAI text-embedding-3-small
│   │   ├── vector_store.py          # ChromaDB / Pinecone + distance scores
│   │   └── llm.py                   # GPT-4o with confidence gate + fallback
│   └── scraper/
│       ├── scraper.py               # Async httpx + BeautifulSoup
│       └── cleaner.py               # ftfy, dedup, normalisation
├── frontend/
│   └── src/
│       ├── App.jsx                  # Chat shell + header + disclaimer
│       └── components/
│           ├── ChatThread.jsx       # Message bubbles + confidence badge
│           └── ChatInput.jsx        # Textarea + example questions
├── tests/
├── .github/workflows/ci.yml
├── docker-compose.yml
└── .env.example
```

---

## ⚙️ Confidence system

The pipeline scores confidence at two points:

1. **Vector retrieval** – `distance` scores from ChromaDB/Pinecone are compared against `CONFIDENCE_DISTANCE_THRESHOLD` (default `0.45`). If fewer than `MIN_CONFIDENT_CHUNKS` (default `2`) chunks beat the threshold, confidence is `false`.

2. **LLM heuristic** – After generation, the answer text is scanned for uncertainty phrases ("I don't have", "consult a", etc.). If detected, `is_confident` is set to `false`.

When `is_confident` is `false`:
- The model returns the standard "I'm not confident…" fallback message
- The frontend shows an amber ⚠ banner on that message bubble
- No sources are listed (avoids implying endorsement of scraped content)

---

## 🐳 Docker

```bash
docker-compose up --build
```

## 🧪 Tests

```bash
cd backend && pytest ../tests/ -v
```

## 📄 License

MIT
