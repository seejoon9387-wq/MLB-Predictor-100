import streamlit as st
import statsapi
from datetime import datetime
import pytz
from modules.ui_manager import UIManager

def main():
    st.title("⚾ MLB 실시간 경기")
    
    # 데이터 로직 (생략 - 이전과 동일)
    # ...
    
    # 1. 새로고침 버튼 (UI 상단)
    if st.button("🔄 실시간 경기정보 새로고침"):
        st.session_state.games = fetch_data()
        st.rerun()

    # 2. 카드 클릭 처리 함수
    def show_details(game):
        st.session_state.selected_game = game

    # 3. UI 렌더링
    UIManager.render_game_navbar(st.session_state.games, show_details)

    # 4. 카드 클릭 시 상세 정보 출력 (Expander)
    if 'selected_game' in st.session_state:
        g = st.session_state.selected_game
        with st.expander(f"📍 {g['away_name']} vs {g['home_name']} 상세 정보", expanded=True):
            info = fetch_details(g['id']) # 상세 데이터 가져오기
            st.write(info)

if __name__ == "__main__":
    main()
