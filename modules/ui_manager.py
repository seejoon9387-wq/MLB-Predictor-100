import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 상단 정렬 및 버튼 고정 (고정된 너비 사용)
        st.markdown("""
            <style>
                .nav-container { display: flex; justify-content: center; align-items: center; gap: 40px; margin-bottom: 20px; }
                .game-card { 
                    border: 1px solid #d1d5db; border-radius: 12px; padding: 15px; 
                    text-align: center; background: #ffffff; height: 170px; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
            </style>
        """, unsafe_allow_html=True)

        # 페이지네이션
        items_per_page = 6
        start = st.session_state.get('current_page', 0) * items_per_page
        page_games = game_data_list[start:start + items_per_page]

        # 버튼 영역 (고정)
        col1, col2, col3 = st.columns([1, 8, 1])
        with col1:
            if st.button("◀"):
                if st.session_state.get('current_page', 0) > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
        with col3:
            if st.button("▶"):
                st.session_state.current_page = st.session_state.get('current_page', 0) + 1
                st.rerun()

        # 2. 카드 배치 (6개 컬럼 고정)
        cols = st.columns(6) 
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 고정된 카드 디자인 클래스 적용
                    st.markdown(f"""
                        <div class="game-card">
                            <div style="font-size: 11px; color: #6b7280; font-weight: bold;">{game.get('display_date', '')}</div>
                            <div style="font-size: 16px; font-weight: 800; color: #dc2626; margin: 8px 0;">{game.get('display_time', '')}</div>
                            <div style="font-size: 12px; font-weight: 700; margin-bottom: 4px;">{game.get('away_name', 'AWAY')}</div>
                            <div style="font-size: 12px; font-weight: 700;">{game.get('home_name', 'HOME')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("상세보기", key=f"btn_{game.get('game_id', i)}"):
                        st.session_state.selected_game_id = game.get('game_id')
                        st.rerun()
