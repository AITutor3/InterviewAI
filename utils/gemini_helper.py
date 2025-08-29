"""
Gemini API helper functions for resume analysis
"""
from typing import Dict
import re
import json
import google.generativeai as genai



def analyze_resume_with_gemini(api_key: str, resume_text: str, job_description: str) -> Dict[str, str]:
    """
    Analyze resume and job description using Gemini API
    
    Args:
        api_key: Gemini API key
        resume_text: Text content of the resume
        job_description: Job description text
        
    Returns:
        Dictionary containing analysis results using korean (probability, match_rate, feedback)
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        prompt = f"""
        다음 이력서와 채용 공고를 분석하여 아래 항목을 한국어로 자세히 작성하세요:

        1. 합격 가능성 (0-100%)
        2. 이력서와 채용 공고 간의 적합도 (0-100%)
        3. 전반적인 피드백과 개선 제안

        응답은 반드시 다음 정확한 키를 가진 JSON 형식으로만 작성하세요:
        - "probability" (숫자만)
        - "match_rate" (숫자만)
        - "feedback" (상세한 한국어 텍스트)

        === RESUME ===
        {resume_text}

        === JOB DESCRIPTION ===
        {job_description}
        """
        
        response = model.generate_content(prompt)
        
        # Extract JSON from the response
        json_str = re.search(r'\{.*\}', response.text, re.DOTALL)
        if json_str:
            return json.loads(json_str.group())
        
        return {
            "probability": "Error in analysis",
            "match_rate": "Error in analysis",
            "feedback": "분석 결과를 파싱하지 못했습니다. 다시 시도해 주세요."
        }
            
    except Exception as e:
        return {
            "probability": "Error",
            "match_rate": "Error",
            "feedback": f"오류가 발생했습니다: {str(e)}"
        }


def generate_interview_questions(
    api_key: str,
    resume_text: str,
    job_role: str,
    company_info: str,
) -> Dict[str, list]:
    """Generate common and resume-based interview questions.

    Returns dict with keys: common_questions (list[str]), resume_questions (list[str])
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        prompt = f"""
        당신은 전문 면접관입니다. 아래 기준에 따라 간결한 한국어 면접 질문을 두 목록으로 작성하세요:

        1) 대부분의 직무에 공통적으로 적용 가능한 질문 (행동 기반 + 필요 시 일반 기술 질문)
        2) 지원자의 이력서, 선택한 직무/회사 정보를 바탕으로 한 맞춤 질문

        제약 사항:
        - 각 목록당 6~8개 항목
        - 답변 없이 질문만 작성
        - 질문은 짧고 핵심적으로 작성

        응답은 반드시 다음 JSON 형식으로만 제출하세요:
        {{
          "common_questions": ["q1", "q2", ...],
          "resume_questions": ["q1", "q2", ...]
        }}

        === JOB ROLE ===
        {job_role}

        === COMPANY INFO ===
        {company_info}

        === RESUME ===
        {resume_text}
        """

        response = model.generate_content(prompt)
        json_match = re.search(r"\{[\s\S]*\}", response.text)
        if json_match:
            data = json.loads(json_match.group())
            # Ensure keys exist and are lists
            return {
                "common_questions": list(data.get("common_questions", [])),
                "resume_questions": list(data.get("resume_questions", [])),
            }

        return {
            "common_questions": [],
            "resume_questions": [],
        }

    except Exception as e:
        return {
            "common_questions": [f"질문 생성 중 오류가 발생했습니다: {str(e)}"],
            "resume_questions": [],
        }


def generate_model_answers(
    api_key: str,
    resume_text: str,
    job_role: str,
    company_info: str,
    questions: list[str],
) -> list[str]:
    """Generate concise Korean model answers for the given questions.

    Returns a list of answers aligned by index with the input questions. On error, returns empty list.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        joined_questions = "\n".join([f"- {q}" for q in questions])
        prompt = f"""
        다음 지원자 정보를 참고하여 각 질문에 대한 모범답안을 한국어로 간결하게 작성하세요.
        각 답변은 3~5문장 이내로 핵심만 담아주세요.

        응답은 반드시 다음 JSON 형식으로만 제출하세요:
        {{"answers": ["a1", "a2", ...]}}  # 질문 리스트와 동일한 순서/길이

        === 직무 ===
        {job_role}

        === 회사/팀 정보 ===
        {company_info}

        === 이력서 ===
        {resume_text}

        === 질문 목록 ===
        {joined_questions}
        """

        response = model.generate_content(prompt)
        json_match = re.search(r"\{[\s\S]*\}", response.text)
        if json_match:
            data = json.loads(json_match.group())
            answers = list(data.get("answers", []))
            # ensure alignment length
            if len(answers) < len(questions):
                answers += [""] * (len(questions) - len(answers))
            return answers[: len(questions)]

        return [""] * len(questions)

    except Exception:
        return [""] * len(questions)
