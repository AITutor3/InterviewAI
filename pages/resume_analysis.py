"""
이력서 분석 페이지
이력서 업로드 및 분석 기능을 처리합니다
"""
import streamlit as st
from utils.gemini_helper import analyze_resume_with_gemini
from utils.file_processor import process_uploaded_file

def show():
    """이력서 분석 페이지 렌더링"""
    st.title("📄 이력서 & 채용 공고 분석")
    st.markdown("---")
    
    with st.form("resume_form"):
        # API Key Input
        api_key = st.text_input("🔑 Gemini API 키를 입력하세요", type="password")
        
        # Resume File Upload
        uploaded_file = st.file_uploader(
            "📄 이력서 업로드 (PDF, DOCX, TXT)", 
            type=['pdf', 'docx', 'txt']
        )
        
        # Process file upload (manual paste 제거: 업로드만 허용)
        resume_text = ""
        file_status = ""
        
        if uploaded_file is not None:
            resume_text, file_status = process_uploaded_file(uploaded_file, api_key=api_key)
            
            if file_status.startswith("Successfully"):
                st.success(file_status)
            elif file_status:
                st.info(file_status)
        
        # Job Description Input
        job_description = st.text_area(
            "💼 채용 공고 내용을 입력하세요",
            placeholder="지원하려는 채용 공고의 내용을 붙여넣으세요...",
            height=200
        )
        
        submitted = st.form_submit_button("이력서 분석")
        
        if submitted:
            if not api_key or (not resume_text and not uploaded_file) or not job_description:
                st.warning("모든 필드를 입력하고 이력서를 업로드해 주세요.")
            else:
                with st.spinner("이력서와 채용 공고를 분석하는 중..."):
                    try:
                        analysis = analyze_resume_with_gemini(
                            api_key, 
                            resume_text or "", 
                            job_description
                        )
                        
                        # Display results in cards
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric(
                                "✅ 합격 가능성", 
                                f"{analysis.get('probability', 'N/A')}%"
                            )
                            
                        with col2:
                            st.metric(
                                "📊 이력서-직무 적합도", 
                                f"{analysis.get('match_rate', 'N/A')}%"
                            )
                        
                        st.markdown("---")
                        st.subheader("📋 상세 피드백")
                        st.write(analysis.get('feedback', '피드백이 없습니다.'))
                        
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {str(e)}")
