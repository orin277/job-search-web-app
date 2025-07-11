from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies.interview import get_interview_service
from app.schemas.interview import CandidateAnswer, InterviewFeedback, InterviewRequest, InterviewResponse, InterviewSession
from app.services.interview_service import InterviewService


router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)


@router.post("/interviews/start")
async def start_interview(
    request: InterviewRequest, 
    interview_service: InterviewService = Depends(get_interview_service)
) -> InterviewResponse:
    return await interview_service.start_interview(request)

@router.post("/interviews/answer")
async def submit_answer(
    answer_request: CandidateAnswer, 
    interview_service: InterviewService = Depends(get_interview_service)
) -> InterviewResponse:
    return await interview_service.get_next_question(answer_request)


@router.get("/interviews/{session_id}/feedback")
async def get_interview_feedback(
    session_id: str,
    interview_service: InterviewService = Depends(get_interview_service)
) -> InterviewFeedback:
    return await interview_service.get_final_feedback(session_id)


@router.delete("/interviews/{session_id}")
async def cancel_interview(
    session_id: str,
    interview_service: InterviewService = Depends(get_interview_service)
) -> dict:
    await interview_service.cancel_interview(session_id)
    return {"message": "cancel", "session_id": session_id}