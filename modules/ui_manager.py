import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        """페이지당 6개 경기를 보여주는 내비게이션 바"""
        # 페이지당 6개로 수정
        items_per_page = 6
        total_pages = (len(game_data_list) + items_per_page - 1) // items_per_page

        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0

        # [이전] [6개 경기 목록] [다음] 레이아웃
        cols = st.columns([0.5, 10, 0.5])
        
        with cols[0]:
            if st.button("◀"):
                st.session_state.current_page = max(0, st.session_state.current_page - 1)
        
        with cols[2]:
            if st.button("▶"):
                st.session_state.current_page = min(total_pages - 1, st.session_state.current_page + 1)

        # 현재 페이지 데이터 슬라이싱
        start = st.session_state.current_page * items_per_page
        end = start + items_per_page
        page_games = game_data_list[start:end]

        # 6개 경기 카드 렌더링
        with cols[1]:
            game_cols = st.columns(items_per_page)
            for i, game in enumerate(page_games):
                with game_cols[i]:
                    st.markdown(f"""
                        <div style="background:#262730; border:1px solid #454545; border-radius:8px; padding:6px; text-align:center; color:white; font-size:10px;">
                            <div style="color:#777; margin-bottom:4px;">종료</div>
                            <div style="display:flex; justify-content:space-between; padding:0 2px;">
                                <span>{game['away_name']}</span> <b>{game['away_score']}</b>
                            </div>
                            <div style="display:flex; justify-content:space-between; padding:0 2px;">
                                <span>{game['home_name']}</span> <b>{game['home_score']}</b>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            # 데이터가 6개보다 적을 경우 빈 공간 채우기 (정렬 유지)
            for _ in range(items_per_page - len(page_games)):
                st.empty()
