import streamlit as st
import statsapi
from datetime import datetime
import pytz
from modules.ui_manager import UIManager

def fetch_data():
    raw_games = statsapi.schedule(date=datetime.now().strftime('%Y-%m-%d'))
    games = []
    for g in raw_games:
        dt = datetime.strptime(g['game_datetime'], "%Y-%m-%dT%H:%M:%SZ")
        dt = dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Seoul'))
        games.append({
            "display_date": g['game_date'],
            "display_time": dt.strftime("%H:%M"),
            "away_name": g['away_name'],
            "away_score": g.get('away_score', 0),
            "home_name": g['home_name'],
            "home_score": g.get('home_score', 0)
        })
    return games

def main():
    st.title("⚾ MLB 실시간 경기")
    
    if 'games' not in st.session_state:
        st.session_state.games = fetch_data()
    
    def refresh():
        # 데이터 업데이트 중 스피너 표시
        with st.spinner('실시간 정보를 불러오는 중입니다...'):
            st.session_state.games = fetch_data()
        st.rerun()

    UIManager.render_game_navbar(st.session_state.games, refresh)

if __name__ == "__main__":
    main()
