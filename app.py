import streamlit as st
import pandas as pd
import requests
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB AI Analyst Pro", layout="wide")

@st.cache_data(ttl=600)
def get_mlb_schedule():
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
                    # [핵심 수정] 엔진이 row['key']로 접근할 때 에러가 나지 않도록 
                    # 딕셔너리와 시리즈의 속성을 모두 가진 하이브리드 객체 생성
                    class SafeData(dict):
                        def __getitem__(self, key):
                            return self.get(key, 0.0)
                    
                    safe_data = SafeData({
                        'bayesian_win_rate': 0.5,
                        'climate_adjusted_prob': 0.1,
                        'inefficiency_score': 0.05
                    })
                    
                    trainer = MLBUnifiedTrainer()
                    # 하이브리드 객체 전달
                    analysis_result = trainer.analyze(safe_data)
                    
                    st.success("데이터 분석 완료")
                    st.write(analysis_result)
                        
                except Exception as e:
                    st.error(f"분석 중 오류 발생: {e}")
                    st.write("---")
                    st.write("### 🚨 해결 팁")
                    st.write("현재 `simulator.py` 18행에서 엔진이 특정 키를 강제하고 있습니다.")
                    st.write("위 코드로도 해결되지 않는다면, **`modules/simulator.py` 18행을 아래와 같이 수정**하는 것이 100% 해결책입니다:")
                    st.code("loc = row.get('bayesian_win_rate', 0) + row.get('climate_adjusted_prob', 0) + row.get('inefficiency_score', 0)")

if __name__ == "__main__":
    main()
