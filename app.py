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
    
    # UI Manager에 전달할 새로고침 함수
    def refresh():
        st.session_state.is_loading = True # 로딩 시작 표시
        st.rerun()

    # 로딩 중일 때 표시할 부분
    if st.session_state.get('is_loading', False):
        with st.spinner('실시간 정보를 불러오는 중입니다...'):
            st.session_state.games = fetch_data()
            st.session_state.is_loading = False # 로딩 완료
        st.rerun() # 데이터 갱신 후 화면 다시 그림

    UIManager.render_game_navbar(st.session_state.games, refresh)

if __name__ == "__main__":
    main()
