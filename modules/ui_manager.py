import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        """좌우 화살표로 페이지를 넘기는 경기 내비게이션"""
        # 1. 페이지당 경기 수 설정
        items_per_page = 5
        total_pages = (len(game_data_list) + items_per_page - 1) // items_per_page

        # 2. 세션 상태 초기화 (페이지 번호 기억)
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0

        # 3. 레이아웃: [이전] [경기목록] [다음]
        cols = st.columns([1, 10, 1])
        
        with cols[0]:
            if st.button("◀"):
                st.session_state.current_page = max(0, st.session_state.current_page - 1)
        
        with cols[2]:
            if st.button("▶"):
                st.session_state.current_page = min(total_pages - 1, st.session_state.current_page + 1)

        # 4. 현재 페이지의 경기만 슬라이싱
        start = st.session_state.current_page * items_per_page
        end = start + items_per_page
        page_games = game_data_list[start:end]

        # 5. 경기 카드 렌더링
        with cols[1]:
            game_cols = st.columns(len(page_games))
            for i, game in enumerate(page_games):
                with game_cols[i]:
                    st.markdown(f"""
                        <div style="background:#262730; border:1px solid #454545; border-radius:10px; padding:8px; text-align:center; color:white; font-size:11px;">
                            <div style="color:#888;">종료</div>
                            <div style="display:flex; justify-content:space-between;"><b>{game['away_name']}</b> {game['away_score']}</div>
                            <div style="display:flex; justify-content:space-between;"><b>{game['home_name']}</b> {game['home_score']}</div>
                        </div>
                    """, unsafe_allow_html=True)
