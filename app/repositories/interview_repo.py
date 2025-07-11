

from typing import Protocol

import redis

from app.schemas.interview import InterviewSession


class InterviewRepository(Protocol):
    async def save(self, session_id: str, session: InterviewSession, ttl: int):
        ...

    async def get(self, session_id: str):
        ...

    async def delete(self, session_id: str):
        ...


class RedisInterviewRepository:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.prefix = "job_search:session:"

    def _key(self, session_id: str) -> str:
        return f"{self.prefix}{session_id}"

    async def save(self, session_id: str, session: InterviewSession, ttl: int = 7200):
        data = session.model_dump_json()
        await self.redis.set(self._key(session_id), data, ex=ttl)

    async def get(self, session_id: str) -> InterviewSession | None:
        raw = await self.redis.get(self._key(session_id))
        if raw is None:
            return None
        return InterviewSession.model_validate_json(raw)

    async def delete(self, session_id: str):
        await self.redis.delete(self._key(session_id))