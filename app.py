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
    
    # 상단 버튼 영역
    col_btn, col_nav = st.columns([2, 5])
    
    with col_btn:
        # 버튼을 누르는 순간 스피너가 즉시 노출됨
        if st.button("🔄 실시간 경기정보 새로고침"):
            with st.spinner('실시간 경기 정보를 불러오는 중입니다...'):
                st.session_state.games = fetch_data()
            st.success('최신 데이터 업데이트 완료!')

    # 데이터 초기화
    if 'games' not in st.session_state:
        st.session_state.games = fetch_data()

    # 페이지네이션 네비게이션
    with col_nav:
        c1, _, c2 = st.columns([1, 8, 1])
        with c1:
            if st.button("◀"):
                if st.session_state.current_page > 0: st.session_state.current_page -= 1
        with c2:
            if st.button("▶"):
                st.session_state.current_page += 1

    # 화면 렌더링
    UIManager.render_game_navbar(st.session_state.games)

if __name__ == "__main__":
    main()
