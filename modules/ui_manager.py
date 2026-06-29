import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 스타일 정의 (카드 가로 확장을 위해 margin 좌우 0 설정)
        st.markdown("""
            <style>
                .nav-btn { display: flex; justify-content: center; align-items: center; }
                .game-card { 
                    border: 1px solid #d1d5db; 
                    border-radius: 12px; 
                    padding: 12px; 
                    text-align: center; 
                    background: #ffffff; 
                    height: 160px; 
                    margin: 0 4px; /* 카드가 서로 너무 붙지 않게 */
                    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
                }
            </style>
        """, unsafe_allow_html=True)

        items_per_page = 6
        start = st.session_state.get('current_page', 0) * items_per_page
        page_games = game_data_list[start:start + items_per_page]

        # 2. 버튼 영역 (최상단 정렬)
        col1, col2, col3 = st.columns([1, 10, 1])
        with col1:
            if st.button("◀", key="prev"):
                if st.session_state.get('current_page', 0) > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
        with col3:
            if st.button("▶", key="next"):
                st.session_state.current_page += 1
                st.rerun()

        # 3. 카드 6개 가로 배치 (컬럼 비율을 1:1:1:1:1:1 로 고정)
        cols = st.columns(6) 
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 카드 가로 균형을 맞추기 위한 내용 구성
                    st.markdown(f"""
                        <div class="game-card">
                            <div style="font-size: 10px; color: #888; font-weight: bold; margin-bottom: 4px;">{game.get('display_date', '')}</div>
                            <div style="font-size: 15px; font-weight: 900; color: #dc2626; margin-bottom: 10px;">{game.get('display_time', '')}</div>
                            <div style="font-size: 11px; font-weight: 700; color: #333; margin-bottom: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{game.get('away_name', 'AWAY')}</div>
                            <div style="font-size: 11px; font-weight: 700; color: #333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{game.get('home_name', 'HOME')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # 상세보기 버튼 (카드 바로 아래 밀착)
                    if st.button("상세보기", key=f"btn_{game.get('game_id', i)}"):
                        st.session_state.selected_game_id = game.get('game_id')
                        st.rerun()
