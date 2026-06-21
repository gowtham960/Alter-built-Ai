import os
import shutil

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.agents.change_order_agent import analyze_change_order_question
from app.db.database import SessionLocal
from app.parsers.file_parser import SUPPORTED_EXTENSIONS, parse_file
from app.schemas.chat import ChatRequest, ChatResponse

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


UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def chunk_text(text: str, chunk_size: int = 500) -> list:
    """Split text into chunks of roughly chunk_size characters."""
    words = text.split()
    chunks = []
    current = []
    current_len = 0
    for word in words:
        current.append(word)
        current_len += len(word) + 1
        if current_len >= chunk_size:
            chunks.append(" ".join(current))
            current = []
            current_len = 0
    if current:
        chunks.append(" ".join(current))
    return chunks


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    project_id: str = "P-1001",
):
    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail={
                "message": f"Unsupported file type: {extension}",
                "supported_extensions": list(SUPPORTED_EXTENSIONS.keys()),
            },
        )

    saved_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        parsed_result = parse_file(saved_path, file.filename)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse file: {str(error)}",
        )

    # Extract raw text from parsed result
    parsed = parsed_result.get("parsed", {})
    raw_text = ""
    if isinstance(parsed, dict):
        raw_text = parsed.get("text", "") or str(parsed)
    elif isinstance(parsed, str):
        raw_text = parsed

    # Chunk and store in Supabase
    chunks = chunk_text(raw_text)
    session = SessionLocal()
    try:
        for i, chunk in enumerate(chunks):
            session.execute(
                text(
                    """
                    INSERT INTO document_chunks 
                    (project_id, source_filename, source_type, chunk_index, chunk_text)
                    VALUES (:project_id, :filename, :source_type, :chunk_index, :chunk_text)
                    """
                ),
                {
                    "project_id": project_id,
                    "filename": file.filename,
                    "source_type": parsed_result.get("file_type", "Unknown"),
                    "chunk_index": i,
                    "chunk_text": chunk,
                },
            )
        session.commit()
    finally:
        session.close()

    return {
        "message": "File uploaded, parsed, and stored successfully",
        "filename": file.filename,
        "chunks_stored": len(chunks),
        "parsed_result": parsed_result,
    }