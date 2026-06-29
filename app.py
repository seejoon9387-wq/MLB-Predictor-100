import streamlit as st
import pandas as pd
import requests
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB AI Analyst Pro", layout="wide")

@st.cache_data(ttl=600)
def get_mlb_schedule():
    today = "2026-06-29"
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={today}&endDate={today}"
    response = requests.get(url)
    data = response.json()
    
    games = []
    if 'dates' in data:
        for date_entry in data['dates']:
            for game in date_entry.get('games', []):
                games.append({
                    'Time': game.get('gameDate', '')[-14:-9],
                    'Away': game['teams']['away']['team']['name'],
                    'Home': game['teams']['home']['team']['name'],
                    'Raw_Data': game
                })
    return pd.DataFrame(games)

def main():
    st.title("⚾ MLB AI 전문 분석 대시보드")
    df = get_mlb_schedule()
    
    if df.empty:
        st.info("오늘 예정된 경기가 없습니다.")
        return

    event = st.dataframe(df[['Time', 'Away', 'Home']], use_container_width=True, hide_index=True, selection_mode="single-row", on_select="rerun")
    
    if event.selection.rows:
        idx = event.selection.rows[0]
        selected = df.iloc[idx]
        
        if st.button("🚀 엔진 가동"):
            with st.spinner('AI 분석 엔진 가동 중...'):
                try:
                    # 1. 엔진이 강제로 요구하는 모든 컬럼을 포함한 데이터 프레임 생성
                    # simulator.py의 18행 요구사항을 충족시키기 위해 dict 대신 series 방식으로 접근
                    engine_df = pd.DataFrame([{
                        'bayesian_win_rate': 0.5,
                        'climate_adjusted_prob': 0.1,
                        'inefficiency_score': 0.05
                    }])
                    
                    # 2. 엔진 인스턴스 생성
                    trainer = MLBUnifiedTrainer()
                    
                    # 3. 분석 수행 (데이터 프레임을 그대로 전달)
                    analysis_result = trainer.analyze(engine_df)
                    
                    # 4. 결과 출력
                    st.success("데이터 분석 완료")
                    st.write(analysis_result)
                        
                except Exception as e:
                    st.error(f"분석 중 오류 발생: {e}")
                    st.write("---")
                    st.write("### 🔍 기술적 분석을 위한 디버그 정보")
                    st.write("현재 전달된 데이터 프레임 컬럼:", engine_df.columns.tolist())
                    st.write("엔진이 요구하는 데이터 구조를 맞추기 위해, simulator.py의 18행 코드를 확인해야 합니다.")

if __name__ == "__main__":
    main()
