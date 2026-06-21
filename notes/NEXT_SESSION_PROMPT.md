# Alter Built AI - Next Session Prompt

## Current Status
The project is fully working locally with:
- FastAPI backend connected to Supabase
- React frontend with upload UI and chat
- Groq AI generating recommendations
- RAG evaluation scoring 95%+
- Document upload pipeline storing chunks in Supabase

## GitHub Repo
https://github.com/gowtham960/Alter-built-Ai

## Next Task: Deployment
1. Deploy frontend to Vercel
   - Connect GitHub repo
   - Set VITE_API_URL to Render backend URL

2. Deploy backend to Render
   - Connect GitHub repo
   - Set environment variables: DATABASE_URL, GROQ_API_KEY

## After Deployment
- Multi-project support (project_id per company)
- Supabase Auth for login
- OCR for scanned PDFs

## Local Run Commands
Backend:
cd backend
.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

Frontend:
cd frontend
npm run dev

RAG Evaluation:
cd backend
python evaluate_rag.py