from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel, Field


class InterviewRequest(BaseModel):
    position: str = Field(...)
    duration_minutes: int = Field(default=30, ge=10, le=120)
    specific_topics: List[str] | None = Field(default=None)
    resume: str | None = Field(default=None)
    vacancy: str | None = Field(default=None)


class InterviewResponse(BaseModel):
    session_id: str
    interviewer_message: str
    interview_status: str


class CandidateAnswer(BaseModel):
    session_id: str
    answer: str
    

class InterviewFeedback(BaseModel):
    session_id: str
    overall_score: float
    technical_score: float | None = None
    communication_score: float
    problem_solving_score: float | None = None
    cultural_fit_score: float | None = None
    strengths: List[str]
    areas_for_improvement: List[str]
    detailed_feedback: str


class InterviewSession(BaseModel):
    position: str
    current_question: int
    total_questions: int
    conversation_history: List[Dict]
    start_time: datetime
    status: str
    specific_topics: List[str] | None = None
    resume: str | None = None
    vacancy: str | None = None