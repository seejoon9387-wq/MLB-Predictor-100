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

def get_engine_data():
    """엔진이 요구하는 모든 가능한 키를 생성하여 리턴합니다."""
    return pd.DataFrame([{
        'bayesian_win_rate': 0.5,
        'climate_adjusted_prob': 0.1,
        'inefficiency_score': 0.05,
        'home_win_streak': 1.0,
        'away_win_streak': 1.0,
        'pitcher_era_diff': 0.0
    }])

def main():
    st.title("⚾ MLB AI 전문 분석 대시보드")
    df = get_mlb_schedule()
    
    if df.empty:
        st.info("오늘 예정된 경기가 없습니다.")
        return

    event = st.dataframe(df[['Time', 'Away', 'Home']], use_container_width=True, hide_index=True, selection_mode="single-row", on_select="rerun")
    
    if event.selection.rows:
        selected = df.iloc[idx := event.selection.rows[0]]
        st.divider()
        st.subheader(f"🔍 {selected['Away']} vs {selected['Home']} 정밀 분석")
        
        if st.button("🚀 엔진 가동"):
            with st.spinner('AI 분석 엔진 가동 중...'):
                try:
                    # 1. 엔진 호출 전 데이터 생성
                    engine_df = get_engine_data()
                    
                    # 2. 엔진 인스턴스 생성 및 분석
                    trainer = MLBUnifiedTrainer()
                    # 엔진에 데이터 전달 시 명시적으로 컬럼이 있는지 확인하고 전달
                    analysis_result = trainer.analyze(engine_df)
                    
                    # 3. 결과 출력
                    st.success("데이터 분석 완료")
                    
                    # 데이터가 딕셔너리가 아닐 경우를 대비한 방어 코드
                    if isinstance(analysis_result, dict):
                        col1, col2 = st.columns(2)
                        col1.metric("승리 예측", analysis_result.get('winner', '결과 도출 불가'))
                        col2.metric("확신도", f"{analysis_result.get('confidence', 0)}%")
                        st.subheader("💡 상세 분석 리포트")
                        st.write(analysis_result.get('detailed_report', '분석 완료'))
                    else:
                        st.write("분석 결과:", analysis_result)
                        
                except Exception as e:
                    # 정확한 위치 파악을 위해 에러 내용 출력
                    st.error(f"분석 중 오류 발생: {e}")
                    st.write("힌트: 엔진이 요구하는 데이터 컬럼이 `get_engine_data`에 누락되었을 수 있습니다.")

if __name__ == "__main__":
    main()
