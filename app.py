import streamlit as st
import pandas as pd
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB AI Analyst", layout="wide")

@st.cache_data(ttl=600)
def get_mlb_schedule():
    # 실제 API 데이터 구조에 맞게 생성
    return pd.DataFrame([
        {'Time': '22:35', 'Away': 'Chicago White Sox', 'Home': 'Baltimore Orioles', 'game_pk': 824822},
        {'Time': '22:40', 'Away': 'Pittsburgh Pirates', 'Home': 'Philadelphia Phillies', 'game_pk': 823444}
    ])

def main():
    st.title("⚾ MLB AI 전문 분석 대시보드")
    
    # 1. 경기 일정표 (상단 고정)
    st.subheader("📅 오늘의 경기 일정")
    df = get_mlb_schedule()
    event = st.dataframe(df[['Time', 'Away', 'Home']], use_container_width=True, hide_index=True, selection_mode="single-row", on_select="rerun")
    
    # 2. 분석 실행부
    if event.selection.rows:
        selected_idx = event.selection.rows[0]
        selected_game = df.iloc[selected_idx]
        
        st.divider()
        st.subheader(f"🔍 {selected_game['Away']} vs {selected_game['Home']} 정밀 분석")
        
        if st.button("🚀 엔진 가동"):
            with st.spinner('AI 분석 엔진 가동 중...'):
                try:
                    data_input = {
                        'game_pk': selected_game['game_pk'],
                        'bayesian_win_rate': 0.52,
                        'climate_adjusted_prob': 0.15,
                        'inefficiency_score': 0.08
                    }
                    
                    trainer = MLBUnifiedTrainer()
                    result = trainer.analyze(data_input)
                    
                    st.success("데이터 분석 완료")
                    col1, col2 = st.columns(2)
                    col1.metric("승리 예측", result.get('winner', 'N/A'))
                    col2.metric("확신도", f"{result.get('confidence', 0)}%")
                    st.info(result.get('detailed_report', '분석 결과 없음'))
                    
                except Exception as e:
                    st.error(f"분석 오류: {e}")

if __name__ == "__main__":
    main()
