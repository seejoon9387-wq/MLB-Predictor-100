import streamlit as st
import statsapi
from datetime import datetime
import pytz
from modules.ui_manager import UIManager

def fetch_data():
    raw_games = statsapi.schedule(date=datetime.now().strftime('%Y-%m-%d'))
    games = []
    for g in raw_games:
        # 시간 변환 로직 (양식 고정)
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
    
    # 세션 상태에 데이터 초기화
    if 'games' not in st.session_state:
        st.session_state.games = fetch_data()
    
    # 버튼 클릭 시 실행할 새로고침 함수
    def refresh():
        st.session_state.games = fetch_data()
        st.rerun()

    # UI 렌더링 호출
    UIManager.render_game_navbar(st.session_state.games, refresh)

if __name__ == "__main__":
    main()
