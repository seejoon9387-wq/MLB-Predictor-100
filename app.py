import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz
# 1. 보유하신 분석 모듈 임포트
try:
    from modules.main_trainer import MLBUnifiedTrainer
    trainer = MLBUnifiedTrainer()
except ImportError:
    trainer = None

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
                    'Raw_Data': game # 엔진에 넘길 전체 데이터
                })
    return pd.DataFrame(games)

def main():
    st.title("⚾ MLB AI 전문 분석 대시보드")
    df = get_mlb_schedule()
    
    if df.empty:
        st.info("데이터를 불러올 수 없습니다.")
        return

    event = st.dataframe(df[['Time', 'Away', 'Home']], use_container_width=True, hide_index=True, selection_mode="single-row", on_select="rerun")
    
    if event.selection.rows:
        idx = event.selection.rows[0]
        selected = df.iloc[idx]
        
        st.divider()
        st.subheader(f"🔍 {selected['Away']} vs {selected['Home']} 정밀 분석")
        
        if st.button("🚀 엔진 가동"):
            if trainer is None:
                st.error("분석 엔진(MLBUnifiedTrainer)을 찾을 수 없습니다.")
                return

            with st.spinner('AI 분석 엔진이 데이터를 정밀 추론 중...'):
                # 2. 엔진 가동 (여기가 핵심입니다)
                try:
                    # 엔진에 경기 데이터를 던지고 결과를 받음
                    analysis_result = trainer.analyze(selected['Raw_Data'])
                    
                    # 3. 결과 출력 (엔진에서 반환하는 데이터 구조에 맞게 출력)
                    st.success("데이터 분석 완료")
                    
                    col1, col2 = st.columns(2)
                    col1.metric("승리 예측", analysis_result.get('winner', '무승부'))
                    col2.metric("확신도", f"{analysis_result.get('confidence', 0)}%")
                    
                    st.subheader("💡 상세 분석 리포트")
                    st.write(analysis_result.get('detailed_report', '분석 데이터가 부족합니다.'))
                    
                except Exception as e:
                    st.error(f"엔진 분석 중 오류: {e}")

if __name__ == "__main__":
    main()
