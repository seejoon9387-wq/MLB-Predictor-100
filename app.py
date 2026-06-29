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
            "id": g['game_id'], "display_date": g['game_date'], "display_time": dt.strftime("%H:%M"),
            "away_name": g['away_name'], "away_score": g.get('away_score', 0),
            "home_name": g['home_name'], "home_score": g.get('home_score', 0)
        })
    return games

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 실시간 경기")
    
    if 'games' not in st.session_state: st.session_state.games = fetch_data()
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    # 1. 상단 제어 영역 (버튼 배치 고정)
    col1, col2, col3 = st.columns([2, 6, 2])
    
    with col1:
        if st.button("🔄 실시간 업데이트"):
            st.session_state.games = fetch_data()
            st.rerun()
            
    with col3:
        n1, n2 = st.columns(2)
        with n1:
            if st.button("◀"):
                if st.session_state.current_page > 0: st.session_state.current_page -= 1
        with n2:
            if st.button("▶"): st.session_state.current_page += 1

    # 2. 카드 영역
    def handle_click(game):
        with st.spinner('정보 로딩 중...'):
            st.session_state.selected_game = game
            st.session_state.details = statsapi.game_data(game['id'])

    UIManager.render_game_navbar(st.session_state.games, handle_click)

    # 3. 상세 정보 영역
    if 'selected_game' in st.session_state and 'details' in st.session_state:
        g = st.session_state.selected_game
        st.divider()
        st.subheader(f"📍 {g['away_name']} vs {g['home_name']} 상세 정보")
        weather = st.session_state.details['gameData']['weather'].get('condition', '정보 없음')
        st.write(f"🌤 **날씨**: {weather}")

if __name__ == "__main__":
    main()
