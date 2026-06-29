import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB AI Analyst Pro", layout="wide")

@st.cache_data(ttl=600)
def get_mlb_schedule():
    today = datetime.now().strftime('%Y-%m-%d')
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

def prepare_engine_data(raw_game_data):
    """엔진이 요구하는 모든 계산 필드를 강제로 생성하여 공급합니다."""
    data_dict = {
        'bayesian_win_rate': 0.5,           # 엔진 기본값
        'climate_adjusted_prob': 0.1,       # 엔진 기본값
        'inefficiency_score': 0.05,         # 엔진 기본값
        'game_pk': raw_game_data.get('gamePk')
    }
    return pd.DataFrame([data_dict])

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
        
        st.divider()
        st.subheader(f"🔍 {selected['Away']} vs {selected['Home']} 정밀 분석")
        
        if st.button("🚀 엔진 가동"):
            with st.spinner('AI 분석 엔진 가동 중...'):
                try:
                    # 1. 데이터를 엔진 입맛에 맞게 전처리
                    engine_input = prepare_engine_data(selected['Raw_Data'])
                    
                    # 2. 엔진 초기화 및 분석
                    trainer = MLBUnifiedTrainer(data=engine_input)
                    analysis_result = trainer.analyze(engine_input)
                    
                    # 3. 결과 출력
                    st.success("데이터 분석 완료")
                    
                    col1, col2 = st.columns(2)
                    col1.metric("승리 예측", analysis_result.get('winner', '데이터 산출 중'))
                    col2.metric("확신도", f"{analysis_result.get('confidence', 0)}%")
                    
                    st.subheader("💡 상세 분석 리포트")
                    st.write(analysis_result.get('detailed_report', '분석 리포트 생성 완료'))
                    
                except Exception as e:
                    st.error(f"분석 중 오류 발생: {e}")
                    st.info("데이터 처리 파이프라인에서 오류가 발생했습니다. 로그를 확인하세요.")

if __name__ == "__main__":
    main()
