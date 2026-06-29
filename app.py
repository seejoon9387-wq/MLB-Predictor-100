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

    # 새로고침 버튼
    if st.button("🔄 실시간 업데이트"):
        st.session_state.games = fetch_data()
        st.rerun()

    # 화살표(좌) + 카드(6개) + 화살표(우) 배치
    layout_cols = st.columns([0.5, 6, 0.5])
    
    with layout_cols[0]:
        st.write("") # 간격 조정
        st.write("")
        if st.button("◀"):
            if st.session_state.current_page > 0: st.session_state.current_page -= 1
            st.rerun()
            
    with layout_cols[1]:
        def handle_click(game):
            with st.spinner('정보 로딩 중...'):
                st.session_state.selected_game = game
                st.session_state.details = statsapi.game_data(game['id'])
        UIManager.render_game_navbar(st.session_state.games, handle_click)

    with layout_cols[2]:
        st.write("") # 간격 조정
        st.write("")
        if st.button("▶"):
            st.session_state.current_page += 1
            st.rerun()

    # 상세 정보 영역
    if 'selected_game' in st.session_state and 'details' in st.session_state:
        g = st.session_state.selected_game
        st.divider()
        st.subheader(f"📍 {g['away_name']} vs {g['home_name']} 상세 정보")
        weather = st.session_state.details['gameData']['weather'].get('condition', '정보 없음')
        st.write(f"🌤 **날씨**: {weather}")

if __name__ == "__main__":
    main()
