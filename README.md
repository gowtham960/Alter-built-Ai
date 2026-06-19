# Alter Built AI

**Agentic RAG for Construction Change-Order Intelligence**

Alter Built AI is a portfolio project that analyzes construction project changes using multiple sources such as contract clauses, project schedules, site notes, weather records, RFIs, and change-order history.

## What the app does

A user can ask questions like:

> Rain delayed concrete work for 3 days. Can we request a schedule extension?

The agent checks multiple sources and returns:

- Recommendation
- Supporting evidence
- Source list
- Confidence level
- Suggested next action

## Tech Stack

- Frontend: React + Vite
- Backend: FastAPI
- Database: Supabase/Postgres later
- Vector Search: Supabase pgvector later
- LLM: OpenAI API later
- Deployment: Vercel + Render later

## Current MVP Status

This starter version includes:

- FastAPI backend
- React frontend
- Mock agent response
- SQL schema and seed data
- Sample contract text
- Progress tracker
- Learning notes
- Git workflow notes

## Run Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## GitHub Setup

```bash
git init
git add .
git commit -m "Initial Alter Built AI starter project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/alter-built-ai.git
git push -u origin main
```
