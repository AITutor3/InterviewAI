"""
Interview AI Assistant - Main Application
"""
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Interview AI Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)
from pages.generate_question import show as show_generate_questions
from pages.resume_analysis import show as show_resume_analysis

# Hide the sidebar completely
def main():
    """Render app with tabs; default tab is Resume Analysis"""
    st.markdown("# 👨‍💻 인터뷰 AI 어시스턴트")
    st.markdown("아래 탭을 사용해 이동하세요.")

    # Remove the sidebar and its toggle from the UI entirely
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        [data-testid="collapsedControl"] {display: none !important;}
        header [data-testid="baseButton-headerNoPadding"] {display: none !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["📄 이력서 분석", "🧠 면접 질문 생성"])

    with tab1:
        show_resume_analysis()
    with tab2:
        show_generate_questions()

    # 기능 섹션
    st.markdown("---")
    st.markdown("## ✨ 주요 기능")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="feature-icon">🤖</div>', unsafe_allow_html=True)
            st.markdown("#### AI 기반 분석")
            st.markdown("이력서와 채용 공고의 적합도 및 상세 피드백을 제공합니다.")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="feature-icon">📊</div>', unsafe_allow_html=True)
            st.markdown("#### 적합도 점수")
            st.markdown("보유 역량과 경력이 직무 요구사항에 얼마나 부합하는지 확인하세요.")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="feature-icon">🎯</div>', unsafe_allow_html=True)
            st.markdown("#### 개인화 피드백")
            st.markdown("이력서 개선과 면접 대비를 위한 실행 가능한 제안을 받으세요.")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 푸터
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6B7280; margin-top: 2rem;">
        <p>© 2024 인터뷰 AI 어시스턴트. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
