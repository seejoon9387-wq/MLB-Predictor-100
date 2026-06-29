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
            "id": g['game_id'],
            "display_date": g['game_date'],
            "display_time": dt.strftime("%H:%M"),
            "away_name": g['away_name'],
            "away_score": g.get('away_score', 0),
            "home_name": g['home_name'],
            "home_score": g.get('home_score', 0)
        })
    return games

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 실시간 경기")
    
    # 세션 상태 초기화
    if 'games' not in st.session_state: st.session_state.games = fetch_data()
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    # 상단 컨트롤
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🔄 새로고침"):
            st.session_state.games = fetch_data()
            st.rerun()

    # 상세 정보 로드 함수 (클릭 시 실행)
    def handle_card_click(game):
        with st.spinner('실시간 경기 상세 정보를 불러오는 중...'):
            st.session_state.selected_game = game
            st.session_state.details = statsapi.game_data(game['id'])

    # UI 렌더링
    UIManager.render_game_navbar(st.session_state.games, handle_card_click)

    # 상세 정보 표시
    if 'selected_game' in st.session_state:
        g = st.session_state.selected_game
        details = st.session_state.details
        st.divider()
        st.subheader(f"📍 {g['away_name']} vs {g['home_name']} 상세 정보")
        weather = details['gameData']['weather'].get('condition', '정보 없음')
        st.write(f"🌤 **날씨**: {weather}")
        # 투수/라인업 등 추가 정보 구현 가능

if __name__ == "__main__":
    main()
