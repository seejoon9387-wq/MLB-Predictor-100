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
    st.title("⚾ MLB 실시간 경기")
    
    # 1. 제어 영역 (버튼 및 네비게이션)
    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("🔄 실시간 경기정보 새로고침"):
            st.session_state.games = fetch_data()
            st.rerun()
    with col_b:
        nav_c1, nav_c2 = st.columns([1, 1])
        with nav_c1:
            if st.button("◀ 이전"):
                if st.session_state.get('current_page', 0) > 0: st.session_state.current_page -= 1
        with nav_c2:
            if st.button("다음 ▶"):
                st.session_state.current_page += 1

    # 2. 카드 영역 (UIManager 호출)
    if 'games' not in st.session_state: st.session_state.games = fetch_data()
    UIManager.render_game_navbar(st.session_state.games, lambda g: st.session_state.update(selected_game=g))

    # 3. 상세 정보 영역 (카드 클릭 시)
    if 'selected_game' in st.session_state:
        g = st.session_state.selected_game
        with st.expander(f"📍 {g['away_name']} vs {g['home_name']} 실시간 상세 정보", expanded=True):
            try:
                info = statsapi.game_data(g['id'])
                weather = info['gameData']['weather'].get('condition', '정보 없음')
                st.write(f"🌤 **날씨**: {weather}")
            except:
                st.write("상세 정보를 불러올 수 없습니다.")

if __name__ == "__main__":
    main()
