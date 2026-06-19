from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.change_order_agent import analyze_change_order_question

app = FastAPI(title="Alter Built AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {
        "app": "Alter Built AI",
        "status": "running",
        "message": "Construction change-order agentic RAG starter backend is live.",
    }


@app.post("/ask", response_model=ChatResponse)
def ask_agent(request: ChatRequest):
    return analyze_change_order_question(request.question)
