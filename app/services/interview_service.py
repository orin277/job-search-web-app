from datetime import datetime
import json
from typing import Any, Dict, List
import uuid
from google import genai
from google.genai import types

from app.repositories.interview_repo import InterviewRepository
from app.schemas.interview import CandidateAnswer, InterviewFeedback, InterviewRequest, InterviewResponse, InterviewSession

from app.core.config import settings
from app.utils.interview import get_feedback_prompt, get_response_from_json, get_system_prompt


class InterviewService:
    def __init__(self, interview_repo: InterviewRepository):
        self.interview_repo = interview_repo
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.5-flash"
    
    async def _get_answer(self, system_prompt, contents):
        return await self.client.aio.models.generate_content(
            model=self.model,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt
            ),
            contents=contents
        )
    
    def _get_start_interview_session(self, interview_request: InterviewRequest):
        return InterviewSession(
            position = interview_request.position,
            current_question = 1,
            total_questions = 2,
            conversation_history = list(),
            start_time = datetime.now(),
            status = "active",
            specific_topics = interview_request.specific_topics,
            resume = interview_request.resume,
            vacancy = interview_request.vacancy
        )
    
    async def start_interview(self, interview_request: InterviewRequest) -> InterviewResponse:
        system_prompt = get_system_prompt(interview_request.position, 
                                                interview_request.specific_topics, 
                                                interview_request.resume, 
                                                interview_request.vacancy)
        session_id = str(uuid.uuid4())
        interview_session = self._get_start_interview_session(interview_request)

        interview_session.conversation_history.append({"role": "user", "parts": [{"text": "Добрий день! Давайте почнемо співбесіду"}]})

        interviewer_message = await self._get_answer(system_prompt, interview_session.conversation_history)
        
        interview_session.conversation_history.append({"role": "model", "parts": [{"text": interviewer_message.text}]})

        await self.interview_repo.save(session_id, interview_session)
        
        response = InterviewResponse(
            session_id = session_id,
            interviewer_message = interviewer_message.text,
            interview_status = "active"
        )
        return response

    async def get_next_question(self, candidate_answer: CandidateAnswer) -> InterviewResponse:
        interview_session = await self.interview_repo.get(candidate_answer.session_id)
        if interview_session is not None:
            interview_session.conversation_history.append({"role": "user", "parts": [{"text": candidate_answer.answer}]})

            system_prompt = get_system_prompt(interview_session.position, 
                                                    interview_session.specific_topics, 
                                                    interview_session.resume, 
                                                    interview_session.vacancy)

            interviewer_message = await self._get_answer(system_prompt, interview_session.conversation_history)
            
            interview_session.conversation_history.append({"role": "model", "parts": [{"text": interviewer_message.text}]})

            interview_session.current_question += 1

            if interview_session.current_question > interview_session.total_questions:
                interview_session.status = "end"

            await self.interview_repo.save(candidate_answer.session_id, interview_session)
            
            response = InterviewResponse(
                session_id = candidate_answer.session_id,
                interviewer_message = interviewer_message.text,
                interview_status = interview_session.status
            )
            return response
        else:
            raise Exception()

    async def get_final_feedback(self, session_id: str) -> InterviewFeedback:
        session = await self.interview_repo.get(session_id)
        if session is None:
            raise Exception()
        
        session.conversation_history.append({"role": "user", "parts": [{"text": get_feedback_prompt()}]})

        system_prompt = get_system_prompt(session.position, 
                                                session.specific_topics, 
                                                session.resume, 
                                                session.vacancy)
        interviewer_message = await self._get_answer(system_prompt, session.conversation_history)

        feedback_data = get_response_from_json(interviewer_message.text)
        return InterviewFeedback(
            session_id=session_id,
            **feedback_data
        )
    
    async def cancel_interview(self, session_id: str):
        session = await self.interview_repo.get(session_id)
        if session is not None:
            await self.interview_repo.delete(session_id)
        return None