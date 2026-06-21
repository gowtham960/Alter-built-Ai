# Alter Built AI - Learning Notes

## What is RAG?
Retrieval Augmented Generation. Instead of asking an AI to answer from memory,
you first retrieve relevant data from your own sources, then pass that as 
context to the AI to generate an answer grounded in real evidence.

## How this project implements RAG
1. User asks a question
2. Agent detects issue type (weather/design/owner/labor)
3. Agent queries 7 sources: contract, schedule, site notes, weather, 
   RFI logs, change order history, uploaded documents
4. Evidence is passed to Groq as context
5. Groq generates recommendation based only on that evidence

## Key Technologies Learned
- FastAPI — Python web framework for building APIs
- SQLAlchemy — Python ORM for database queries
- Supabase — Postgres database in the cloud
- Groq — Fast LLM API (free tier available)
- React + Vite — Frontend framework
- pgvector — Vector search (planned for next phase)

## Key Design Decisions
- Upload is admin ingestion, not per-question upload
- Agent always searches all sources before answering
- Mock tools kept for contract clause search (not yet in DB)
- document_chunks table stores parsed text for semantic search

## RAG Evaluation Metrics
- Retrieval: Are the right sources being found?
- Relevance: Is the evidence meaningful (not "no match found")?
- Generation: Does the AI use expected domain keywords?
- End-to-End: Are all response fields present and populated?

## Lessons Learned
- Always check which .env file the app is actually reading
- Supabase connection string needs +psycopg2 for SQLAlchemy
- Special characters like @ in passwords break connection URLs
- Groq model names change — check console.groq.com for current models
- Claude Code is powerful but uses API credits fast