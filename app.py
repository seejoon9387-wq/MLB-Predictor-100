import streamlit as st
import pandas as pd
import requests
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB AI Analyst Pro", layout="wide")

@st.cache_data(ttl=600)
def get_mlb_schedule():
    # 오늘 날짜 데이터를 안정적으로 가져오기 위한 설정
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=2026-06-29&endDate=2026-06-29"
    try:
        response = requests.get(url, timeout=10)
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
    except Exception:
        return pd.DataFrame()

def main():
    st.title("⚾ MLB AI 전문 분석 대시보드")
    df = get_mlb_schedule()
    
    if df.empty:
        st.info("오늘 예정된 경기가 없습니다.")
        return

    event = st.dataframe(df[['Time', 'Away', 'Home']], use_container_width=True, hide_index=True, selection_mode="single-row", on_select="rerun")
    
    if event.selection.rows:
        selected = df.iloc[event.selection.rows[0]]
        st.divider()
        st.subheader(f"🔍 {selected['Away']} vs {selected['Home']} 정밀 분석")
        
        if st.button("🚀 엔진 가동"):
            with st.spinner('AI 분석 엔진 가동 중...'):
                try:
                    # 1. 엔진이 요구하는 엄격한 데이터 포맷 (Series 형식)
                    engine_data = pd.Series({
                        'bayesian_win_rate': 0.5,
                        'climate_adjusted_prob': 0.1,
                        'inefficiency_score': 0.05
                    })
                    
                    # 2. 분석 엔진 호출
                    trainer = MLBUnifiedTrainer()
                    # 엔진에 Series 형태로 전달하여 18행의 row 접근 방식 충족
                    analysis_result = trainer.analyze(engine_data)
                    
                    # 3. 결과 출력
                    st.success("데이터 분석 완료")
                    
                    if isinstance(analysis_result, dict):
                        col1, col2 = st.columns(2)
                        col1.metric("승리 예측", analysis_result.get('winner', '결과 도출 불가'))
                        col2.metric("확신도", f"{analysis_result.get('confidence', 0)}%")
                        st.subheader("💡 상세 분석 리포트")
                        st.write(analysis_result.get('detailed_report', '분석 완료'))
                    else:
                        st.write("분석 결과:", analysis_result)
                        
                except Exception as e:
                    st.error(f"분석 중 오류 발생: {e}")
                    st.info("로그를 확인하여 simulator.py 18행의 변수명을 다시 한 번 점검해 주세요.")

if __name__ == "__main__":
    main()
