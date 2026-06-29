import streamlit as st
import pandas as pd
import requests
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB AI Analyst Pro", layout="wide")

@st.cache_data(ttl=300)
def get_mlb_schedule():
    # 실제 MLB 데이터를 가져오는 API 호출
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=2026-06-29&endDate=2026-06-29"
    try:
        response = requests.get(url).json()
        games = []
        for date in response.get('dates', []):
            for game in date.get('games', []):
                games.append({
                    'Time': game.get('gameDate', '')[11:16],
                    'Away': game['teams']['away']['team']['name'],
                    'Home': game['teams']['home']['team']['name'],
                    'game_pk': game['gamePk']
                })
        return pd.DataFrame(games)
    except:
        return pd.DataFrame()

def main():
    st.title("⚾ MLB AI 전문 분석 대시보드")
    
    # 1. 경기 일정표 (높이 400으로 설정하여 전체 리스트 확인 가능)
    st.subheader("📅 오늘의 전체 경기 일정")
    df = get_mlb_schedule()
    
    if not df.empty:
        # 데이터프레임 선택 모드 설정
        event = st.dataframe(
            df[['Time', 'Away', 'Home']], 
            use_container_width=True, 
            height=400, 
            hide_index=True, 
            selection_mode="single-row", 
            on_select="rerun"
        )
        
        # 2. 선택된 경기가 있을 경우 분석 영역 표시
        if event.selection.rows:
            selected_idx = event.selection.rows[0]
            selected_game = df.iloc[selected_idx]
            
            st.divider()
            st.subheader(f"🔍 {selected_game['Away']} vs {selected_game['Home']} 정밀 분석")
            
            if st.button("🚀 엔진 가동"):
                with st.spinner('AI 분석 엔진이 데이터를 정밀 추론 중...'):
                    try:
                        trainer = MLBUnifiedTrainer()
                        data_input = {
                            'game_pk': selected_game['game_pk'],
                            'bayesian_win_rate': 0.52,
                            'climate_adjusted_prob': 0.15,
                            'inefficiency_score': 0.08
                        }
                        result = trainer.analyze(data_input)
                        
                        # 지표 시각화
                        col1, col2 = st.columns(2)
                        col1.metric("승리 예측", result.get('winner', 'N/A'))
                        col2.metric("확신도", f"{result.get('confidence', 0)}%")
                        
                        # 상세 리포트 및 진행률 차트
                        st.markdown("---")
                        st.info(result.get('detailed_report', '분석 데이터 없음'))
                        st.progress(result.get('confidence', 0) / 100)
                        
                    except Exception as e:
                        st.error(f"분석 오류: {e}")
    else:
        st.warning("오늘 예정된 경기가 없거나 데이터를 불러올 수 없습니다.")

if __name__ == "__main__":
    main()
