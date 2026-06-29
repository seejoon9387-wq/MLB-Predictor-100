import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # [최적화 스타일] 카드가 세로로 떨어지는 것을 방지하고 가로로만 나열
        st.markdown("""
            <style>
                .nav-row { display: flex; align-items: center; justify-content: center; gap: 10px; width: 100%; }
                .cards-wrapper { display: flex; flex-direction: row; gap: 10px; }
                .game-card { 
                    width: 140px; height: 100px; border: 1px solid #ddd; 
                    border-radius: 10px; padding: 10px; background: white; 
                    display: flex; flex-direction: column; justify-content: space-between;
                    font-size: 11px; flex-shrink: 0;
                }
            </style>
        """, unsafe_allow_html=True)

        items_per_page = 6
        total_pages = max(1, (len(game_data_list) + items_per_page - 1) // items_per_page)
        if 'current_page' not in st.session_state: st.session_state.current_page = 0

        # [레이아웃] 양 끝 화살표 + 중앙 카드 영역
        cols = st.columns([1, 10, 1])

        with cols[0]:
            if st.button("◀", key="prev"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()

        with cols[1]:
            # 카드들을 하나의 컨테이너로 묶어서 절대 밑으로 떨어지지 않게 함
            st.markdown('<div class="cards-wrapper">', unsafe_allow_html=True)
            start = st.session_state.current_page * items_per_page
            page_games = game_data_list[start:start + items_per_page]
            
            for game in page_games:
                # 카드 디자인 + 보기 버튼이 하나의 묶음으로 처리되도록 함
                st.markdown(f"""
                    <div class="game-card">
                        <div style="font-weight:bold; color:#666;">{game.get('display_date', '')}</div>
                        <div style="display:flex; justify-content:space-between;"><span>{game.get('away_name', 'AWY')}</span> <b>{game.get('away_score', 0)}</b></div>
                        <div style="display:flex; justify-content:space-between;"><span>{game.get('home_name', 'HOM')}</span> <b>{game.get('home_score', 0)}</b></div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("보기", key=f"btn_{game.get('game_id')}"):
                    st.session_state.selected_game_id = game.get('game_id')
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with cols[2]:
            if st.button("▶", key="next"):
                if st.session_state.current_page < total_pages - 1:
                    st.session_state.current_page += 1
                    st.rerun()
