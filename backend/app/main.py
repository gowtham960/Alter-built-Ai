import os
import shutil
from app.parsers.file_parser import parse_file, SUPPORTED_EXTENSIONS
from fastapi import FastAPI, UploadFile, File, HTTPException
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
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads and parses a construction project file.
    Supported formats: PDF, CSV, XLSX, DOCX, TXT.
    """

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

    return {
        "message": "File uploaded and parsed successfully",
        "filename": file.filename,
        "parsed_result": parsed_result,
    }