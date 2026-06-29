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
            "id": g['game_id'], "away_name": g['away_name'], "away_score": g.get('away_score', 0),
            "home_name": g['home_name'], "home_score": g.get('home_score', 0)
        })
    return games

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 실시간 경기")

    if 'games' not in st.session_state: st.session_state.games = fetch_data()
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    if st.button("🔄 새로고침"):
        st.session_state.games = fetch_data()
        st.rerun()

    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.button("◀ 이전"):
            if st.session_state.current_page > 0: st.session_state.current_page -= 1
            st.rerun()
    with col2:
        def handle_card_click(game):
            st.session_state.selected_game = game
            st.session_state.details = statsapi.game_data(game['id'])
            st.rerun()
            
        UIManager.render_game_navbar(st.session_state.games, handle_card_click)
    with col3:
        if st.button("다음 ▶"):
            st.session_state.current_page += 1
            st.rerun()

    if 'selected_game' in st.session_state and 'details' in st.session_state:
        st.divider()
        g = st.session_state.selected_game
        details = st.session_state.details
        st.subheader(f"📍 {g['away_name']} vs {g['home_name']} 실시간 상세 정보")
        try:
            weather = details['gameData']['weather'].get('condition', '정보 없음')
            st.write(f"🌤 **날씨**: {weather}")
        except:
            st.write("상세 정보를 불러오는 중입니다...")

if __name__ == "__main__":
    main()
