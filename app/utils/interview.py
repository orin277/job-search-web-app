

import json


def get_system_prompt(position, specific_topics, resume, vacancy):
    topics_str = ""
    if specific_topics:
        topics_str = f"Особливу увагу приділи темам: {', '.join(specific_topics)}"
    
    resume_str = ""
    if resume:
        resume_str = f"Резюме кандидата: {resume}"

    vacancy_str = ""
    if vacancy:
        vacancy_str = f"Вакансія на яку проводиться співбесіда: {vacancy}"
        
    system_prompt = f"""
        Ти досвідчений інтерв'юер. Твоє завдання – провести технічну співбесіду для позиції {position}. 
        Будь професійним, але доброзичливим. Відповідай лаконічно. Не задавай багато питань одразу. 
        Давай конструктивний зворотний зв'язок.

        {topics_str}
        {resume_str}
        {vacancy_str}
    """
    return system_prompt


def get_feedback_prompt():
    return f"""
        Проаналізуй співбесіду і дай фідбек.
        Поверни відповідь у форматі JSON:
        {{
            "overall_score": 7.5,
            "technical_score": 8.0,
            "communication_score": 7.0,
            "problem_solving_score": 8.5,
            "cultural_fit_score": 7.0,
            "strengths": ["Непогані технічні знання", "Структуровані відповіді"],
            "areas_for_improvement": ["Більше конкретних прикладів", "Розвиток soft skills"],
            "detailed_feedback": "Детальний фідбек...",
        }}
    """

def get_response_from_json(response_text):
    if response_text.startswith("```json") and response_text.endswith("```"):
        json_str = response_text[7:-3].strip()
    else:
        json_str = response_text.strip()

    return json.loads(json_str)