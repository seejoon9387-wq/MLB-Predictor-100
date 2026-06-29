import streamlit as st
import pandas as pd

def apply_custom_css():
    st.markdown("""
        <style>
        /* Sportify 스타일을 위한 커스텀 CSS */
        .main { background-color: #0f1117; }
        .stApp { background-color: #0f1117; }
        .glass-card {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 1rem;
            padding: 1.5rem;
        }
        .scoreboard {
            background: linear-gradient(135deg, #1e2025 0%, #15171c 100%);
            border-radius: 1rem;
            padding: 2rem;
            text-align: center;
        }
        .text-brand { color: #FE7701 !important; }
        </style>
    """, unsafe_allow_html=True)

def main():
    apply_custom_css()
    
    # 1. 상단 스코어보드 영역 (제공해주신 사이트의 헤더/카드 레이아웃 차용)
    st.markdown('<div class="scoreboard">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    col1.metric("Chicago White Sox", "3")
    col2.markdown("### VS")
    col3.metric("Baltimore Orioles", "5")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. 메인 콘텐츠 탭 구조
    tabs = st.tabs(["경기 개요", "상세 지표", "AI 예측"])
    
    with tabs[0]:
        st.subheader("오늘의 경기 정보")
        st.markdown('<div class="glass-card">경기 상태: 종료 (Final)</div>', unsafe_allow_html=True)
        
    with tabs[1]:
        # 여기에 실제 데이터 매핑
        df = pd.DataFrame({
            "항목": ["ERA", "OPS", "AVG"],
            "Home": [3.5, 0.85, 0.27],
            "Away": [4.2, 0.78, 0.25]
        })
        st.table(df)

    with tabs[2]:
        st.subheader("AI 분석 결과")
        # 기존 main_trainer 연동 영역
        st.progress(0.65)
        st.write("AI 모델이 홈팀 Baltimore Orioles의 승리를 65% 확률로 예측합니다.")

if __name__ == "__main__":
    main()
