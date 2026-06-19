from pydantic import BaseModel
from typing import List


class ChatRequest(BaseModel):
    question: str


class EvidenceItem(BaseModel):
    source_type: str
    source_name: str
    detail: str


class ChatResponse(BaseModel):
    recommendation: str
    confidence: str
    answer: str
    evidence: List[EvidenceItem]
    next_action: str
