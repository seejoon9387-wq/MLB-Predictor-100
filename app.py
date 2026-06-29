import streamlit as st
import statsapi # MLB 공식 데이터 라이브러리
from modules.ui_manager import UIManager

# API 호출 결과를 캐싱하여 1분 동안은 다시 호출하지 않게 함 (성능 최적화)
@st.cache_data(ttl=60)
def fetch_mlb_live_data():
    try:
        # 2026년 6월 30일 경기를 불러옵니다.
        # statsapi는 공식 MLB 서버의 데이터를 가져옵니다.
        schedule = statsapi.schedule(date='2026-06-30')
        
        games = []
        for game in schedule:
            games.append({
                'match_time': game['game_time'], 
                'away_name': game['away_name'],
                'away_score': game.get('away_score', 0),
                'home_name': game['home_name'],
                'home_score': game.get('home_score', 0)
            })
        return games
    except Exception as e:
        st.error("데이터 로딩 실패")
        return []

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ 2026년 6월 30일 MLB 공식 실시간 경기")
    
    if st.button("🔄 MLB 서버에서 실시간 업데이트"):
        st.cache_data.clear()
        st.rerun()
        
    games = fetch_mlb_live_data()
    
    if games:
        UIManager.render_game_navbar(games)
    else:
        st.write("오늘 예정된 경기가 없거나 서버 연결에 문제가 있습니다.")
    
if __name__ == "__main__":
    main()
