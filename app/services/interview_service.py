from datetime import datetime
import json
from typing import Any, Dict, List
import uuid
from google import genai
from google.genai import types

from app.schemas.interview import CandidateAnswer, InterviewFeedback, InterviewRequest, InterviewResponse, InterviewSession

from app.core.config import settings
from app.utils.interview import get_feedback_prompt, get_response_from_json, get_system_prompt


interview_sessions: Dict[str, InterviewSession] = {}

class InterviewService:
    def __init__(self):
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

        interview_sessions[session_id] = interview_session

        interviewer_message = await self._get_answer(system_prompt, interview_session.conversation_history)
        
        interview_session.conversation_history.append({"role": "model", "parts": [{"text": interviewer_message.text}]})
        
        response = InterviewResponse(
            session_id = session_id,
            interviewer_message = interviewer_message.text,
            interview_status = "active"
        )
        return response

    async def get_next_question(self, candidate_answer: CandidateAnswer) -> InterviewResponse:
        session_id = candidate_answer.session_id
        if session_id in interview_sessions:
            interview_sessions[session_id].conversation_history.append({"role": "user", "parts": [{"text": candidate_answer.answer}]})

            system_prompt = get_system_prompt(interview_sessions[session_id].position, 
                                                    interview_sessions[session_id].specific_topics, 
                                                    interview_sessions[session_id].resume, 
                                                    interview_sessions[session_id].vacancy)

            interviewer_message = await self._get_answer(system_prompt, interview_sessions[candidate_answer.session_id].conversation_history)
            
            interview_sessions[session_id].conversation_history.append({"role": "model", "parts": [{"text": interviewer_message.text}]})

            interview_sessions[session_id].current_question += 1

            interview_status = "active"
            if interview_sessions[session_id].current_question > interview_sessions[session_id].total_questions:
                interview_status = "end"
            
            response = InterviewResponse(
                session_id = session_id,
                interviewer_message = interviewer_message.text,
                interview_status = interview_status
            )
            return response
        else:
            raise Exception()

    async def get_final_feedback(self, session_id: str) -> InterviewFeedback:
        if session_id not in interview_sessions:
            raise Exception()
        
        session = interview_sessions[session_id]

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
    
    def cancel_interview(self, session_id: str):
        if session_id in interview_sessions:
            interview_sessions.pop(session_id)
        return