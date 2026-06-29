import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 페이지네이션 관리
        items_per_page = 6
        total_pages = max(1, (len(game_data_list) + items_per_page - 1) // items_per_page)
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0

        # 2. 내비게이션 버튼 (상단 독립 영역)
        nav_cols = st.columns([1, 8, 1])
        with nav_cols[0]:
            if st.button("◀ 이전"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
        with nav_cols[2]:
            if st.button("다음 ▶"):
                if st.session_state.current_page < total_pages - 1:
                    st.session_state.current_page += 1
                    st.rerun()

        # 3. 카드 그리드 (6개 고정)
        start = st.session_state.current_page * items_per_page
        page_games = game_data_list[start:start + items_per_page]
        
        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 가독성을 위한 깔끔한 HTML 카드
                    st.markdown(f"""
                        <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px; background: white; margin-bottom: 5px;">
                            <div style="font-size: 10px; color: #6b7280; font-weight: bold; margin-bottom: 5px;">{game.get('display_date', '')}</div>
                            <div style="font-size: 14px; font-weight: 800; color: #111827; margin-bottom: 10px;">{game.get('display_time', '')}</div>
                            <div style="font-size: 12px; font-weight: 700; display: flex; justify-content: space-between;">
                                <span>{game.get('away_name', 'AWY')}</span> <span>{game.get('away_score', 0)}</span>
                            </div>
                            <div style="font-size: 12px; font-weight: 700; display: flex; justify-content: space-between;">
                                <span>{game.get('home_name', 'HOM')}</span> <span>{game.get('home_score', 0)}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("상세보기", key=f"btn_{game.get('game_id', i)}"):
                        st.session_state.selected_game_id = game.get('game_id')
                        st.rerun()
                else:
                    st.write("") # 빈 공간
