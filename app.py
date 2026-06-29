import streamlit as st
import pandas as pd
import requests
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB AI Analyst", layout="wide")

@st.cache_data(ttl=300)
def get_mlb_schedule():
    # 2026-06-29 오늘 날짜의 전체 경기 가져오기
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
    
    # 전체 일정 표시
    df = get_mlb_schedule()
    if not df.empty:
        st.subheader("📅 오늘의 전체 경기 일정")
        # 높이를 늘려 전체 일정이 보이게 설정
        event = st.dataframe(df, use_container_width=True, height=400, hide_index=True, selection_mode="single-row", on_select="rerun")
        
        if event.selection.rows:
            selected_game = df.iloc[event.selection.rows[0]]
            st.divider()
            st.subheader(f"🔍 {selected_game['Away']} vs {selected_game['Home']} 정밀 분석")
            if st.button("🚀 엔진 가동"):
                # 분석 로직 (기존과 동일)
                trainer = MLBUnifiedTrainer()
                result = trainer.analyze({'game_pk': selected_game['game_pk']})
                st.write(result['detailed_report'])
    else:
        st.warning("경기 일정을 불러올 수 없습니다.")

if __name__ == "__main__":
    main()
