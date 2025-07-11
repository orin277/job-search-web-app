

from fastapi import Depends
from redis import Redis
from app.db.database import get_redis_db
from app.repositories.interview_repo import InterviewRepository, RedisInterviewRepository
from app.services.interview_service import InterviewService



def get_interview_repository(
    db: Redis = Depends(get_redis_db)
) -> InterviewRepository:
    return RedisInterviewRepository(db)


def get_interview_service(
    repo: InterviewRepository = Depends(get_interview_repository)
) -> InterviewService:
    return InterviewService(repo)