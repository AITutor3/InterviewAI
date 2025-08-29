"""
면접 질문 생성 페이지
애플리케이션의 질문 생성 탭 화면
"""
import streamlit as st
from utils.file_processor import process_uploaded_file
from utils.gemini_helper import generate_interview_questions, generate_model_answers

def show():
    """면접 질문 생성 페이지 렌더링"""
    # Custom CSS for styling
    st.markdown("""
    <style>
        .main-header {font-size: 2.5rem; font-weight: 700; color: #1E3A8A;}
        .sub-header {font-size: 1.5rem; color: #3B82F6;}
        .card {padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 2rem;}
        .feature-icon {font-size: 2.5rem; margin-bottom: 1rem;}
        .stButton>button {width: 100%; padding: 0.75rem; border-radius: 8px;}
    </style>
    """, unsafe_allow_html=True)
    
    # 면접 질문 생성기
    st.subheader("🧠 면접 질문 생성")
    st.caption("이력서를 제공하고, 역할을 선택한 뒤 회사 정보를 입력하면 질문을 생성합니다.")
    
    with st.form("question_form"):
        api_key = st.text_input("🔑 Gemini API 키", type="password")
        uploaded_file = st.file_uploader(
            "📄 이력서 업로드 (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], key="home_resume"
        )
        job_role = st.selectbox(
            "🎯 직무 선택",
            [
                "IT/소프트웨어 개발",
                "영업/영업관리",
                "마케팅",
                "연구개발(R&D)",
                "기획/전략",
                "데이터 분석/사이언티스트",
                "인사(HR)",
                "재무/회계",
                "생산/품질관리",
                "디자인(UX/UI, 제품)",
            ],
        )
        company_info = st.text_area(
            "🏢 회사/팀 정보",
            placeholder="예: 회사명, 제품/도메인, 기술 스택, 문화, 최근 뉴스 ...",
            height=120,
        )
        # 파일 업로드만 허용 (수동 붙여넣기 제거)
        resume_text = ""
        if uploaded_file is not None:
            extracted, status = process_uploaded_file(uploaded_file, api_key=api_key)
            if status.startswith("Successfully"):
                st.success(status)
                resume_text = extracted or ""
            else:
                st.info(status)
        submitted = st.form_submit_button("질문 생성")
    
    if submitted:
        effective_role = job_role
        if not api_key or not (resume_text.strip()) or not effective_role:
            st.warning("API 키, 이력서, 직무를 모두 입력해주세요.")
        else:
            with st.spinner("면접 질문을 생성하는 중..."):
                result = generate_interview_questions(
                    api_key=api_key,
                    resume_text=resume_text,
                    job_role=effective_role,
                    company_info=company_info,
                )
            # Slice top 5
            common_questions = result.get("common_questions", [])[:5]
            resume_questions = result.get("resume_questions", [])[:5]

            # Generate model answers for each category
            with st.spinner("모범답안을 생성하는 중..."):
                common_answers = generate_model_answers(
                    api_key=api_key,
                    resume_text=resume_text,
                    job_role=effective_role,
                    company_info=company_info,
                    questions=common_questions,
                ) if common_questions else []

                resume_answers = generate_model_answers(
                    api_key=api_key,
                    resume_text=resume_text,
                    job_role=effective_role,
                    company_info=company_info,
                    questions=resume_questions,
                ) if resume_questions else []

            col_q1, col_q2 = st.columns(2)
            with col_q1:
                st.subheader("📚 공통 질문 (Top 5)")
                if common_questions:
                    for i, q in enumerate(common_questions):
                        with st.expander(q):
                            ans = (common_answers[i] if i < len(common_answers) else "").strip()
                            if ans:
                                st.write(ans)
                            else:
                                st.caption("모범답안을 생성하지 못했습니다. 다시 시도해 주세요.")
                else:
                    st.write("생성된 질문이 없습니다.")
            with col_q2:
                st.subheader("🧾 이력서 기반 질문 (Top 5)")
                if resume_questions:
                    for i, q in enumerate(resume_questions):
                        with st.expander(q):
                            ans = (resume_answers[i] if i < len(resume_answers) else "").strip()
                            if ans:
                                st.write(ans)
                            else:
                                st.caption("모범답안을 생성하지 못했습니다. 다시 시도해 주세요.")
                else:
                    st.write("생성된 질문이 없습니다.")
