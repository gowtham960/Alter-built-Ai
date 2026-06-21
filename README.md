# Alter Built AI
**Agentic RAG for Construction Change-Order Intelligence**

Alter Built AI is a live portfolio project that analyzes construction project 
changes using multiple evidence sources including uploaded contracts, project 
schedules, site notes, weather records, RFIs, and change-order history.

## What the app does

A user uploads their project documents, then asks questions like:
> Rain delayed concrete work for 3 days. Can we request a schedule extension?

The agent searches all project sources and returns:
- AI-generated recommendation (eligible / not eligible)
- Supporting evidence from real project data
- Confidence level
- Suggested next action

## Tech Stack

- Frontend: React + Vite
- Backend: FastAPI (Python)
- Database: Supabase (Postgres)
- LLM: Groq (llama-3.3-70b-versatile)
- Document Parsing: pypdf, python-docx, openpyxl, pandas
- Deployment: Vercel (frontend) + Render (backend) — coming soon

## Completed Milestones

- ✅ Milestone 0 — Project setup and GitHub
- ✅ Milestone 1 — FastAPI backend + React frontend working
- ✅ Milestone 2A — Document parsers (PDF, DOCX, XLSX, CSV, TXT)
- ✅ Milestone 3 — Supabase database connected with real project data
- ✅ Milestone 4 — Groq AI-generated recommendations
- ✅ Milestone 5 — Frontend displaying full AI responses with evidence cards
- ✅ Milestone 6 — Document upload pipeline (parse + store in Supabase)
- ✅ Milestone 7 — RAG evaluation system (scoring 95%+)

## RAG Evaluation Results

| Metric | Score |
|---|---|
| Retrieval | 100% |
| Relevance | 82% |
| Generation | 100% |
| End-to-End | 100% |
| **Overall** | **95%+** |

## Run Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
cp .env.example .env         # add DATABASE_URL and GROQ_API_KEY
uvicorn app.main:app --reload
```

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

## Run RAG Evaluation

```bash
cd backend
python evaluate_rag.py
```

## API Endpoints

- `GET /` — Health check
- `POST /ask` — Ask a change-order question
- `POST /upload` — Upload a project document