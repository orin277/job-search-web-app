

from app.services.interview_service import InterviewService


def get_interview_service() -> InterviewService:
    return InterviewService()