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
            "away_name": g['away_name'],
            "away_score": g.get('away_score', 0),
            "home_name": g['home_name'],
            "home_score": g.get('home_score', 0)
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

    # 화살표와 카드 영역
    col_l, col_m, col_r = st.columns([1, 10, 1])
    
    with col_l:
        if st.button("◀ 이전"):
            if st.session_state.current_page > 0: st.session_state.current_page -= 1
            st.rerun()
            
    with col_m:
        UIManager.render_game_navbar(st.session_state.games, lambda g: st.session_state.update(selected_game=g, details=statsapi.game_data(g['id'])))
        
    with col_r:
        if st.button("다음 ▶"):
            st.session_state.current_page += 1
            st.rerun()

    # 상세 정보
    if 'selected_game' in st.session_state:
        st.divider()
        g = st.session_state.selected_game
        st.subheader(f"📍 {g.get('away_name')} vs {g.get('home_name')} 상세 정보")
        st.write("상세 정보가 로드되었습니다.")

if __name__ == "__main__":
    main()
