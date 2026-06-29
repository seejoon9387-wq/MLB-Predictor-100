import streamlit as st
import pandas as pd
from modules.main_trainer import MLBUnifiedTrainer

def main():
    st.set_page_config(page_title="MLB Scoreboard", layout="wide")
    
    # UI 스타일링 (CSS)
    st.markdown("""
        <style>
        .scoreboard { background-color: #0e1117; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #333; }
        .team-name { font-size: 24px; font-weight: bold; }
        .score { font-size: 48px; font-weight: bold; color: #ff4b4b; }
        </style>
    """, unsafe_allow_html=True)

    # 1. 상단 스코어보드 영역
    st.markdown('<div class="scoreboard">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 2])
    c1.markdown('<p class="team-name">Chicago White Sox</p><p class="score">3</p>', unsafe_allow_html=True)
    c2.markdown('<br><h3>VS</h3>', unsafe_allow_html=True)
    c3.markdown('<p class="team-name">Baltimore Orioles</p><p class="score">5</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()

    # 2. 분석 엔진 연동
    sample_data = {'h_era': 3.5, 'a_era': 4.2, 'h_ops': 0.85, 'a_ops': 0.78, 'h_avg': 0.27, 'a_avg': 0.25}
    trainer = MLBUnifiedTrainer()
    result = trainer.analyze(sample_data)
    
    # 3. 상세 분석 UI (표 구조)
    tab1, tab2 = st.tabs(["📊 경기 상세 지표", "📈 AI 승리 예측"])
    
    with tab1:
        st.subheader("상세 경기 데이터")
        df = pd.DataFrame({
            "지표": ["방어율(ERA)", "OPS", "타율(AVG)"],
            "Home(Orioles)": [3.5, 0.85, 0.27],
            "Away(White Sox)": [4.2, 0.78, 0.25]
        })
        st.table(df)
        
    with tab2:
        st.subheader("AI 예측 분석")
        col_a, col_b = st.columns(2)
        col_a.metric("예측 승자", result['winner'])
        col_b.metric("확신도", f"{result['confidence']}%")
        st.progress(result['score'])

if __name__ == "__main__":
    main()
