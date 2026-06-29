import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 완벽한 일렬 배치를 위한 CSS
        st.markdown("""
            <style>
                /* 전체를 감싸는 컨테이너 - 가로 정렬 */
                .navbar-wrapper { display: flex; align-items: center; justify-content: center; gap: 10px; width: 100%; }
                /* 카드들의 영역 */
                .cards-container { display: flex; flex-direction: row; gap: 8px; }
                /* 카드 디자인 */
                .card-box { 
                    width: 140px; height: 85px; border: 1px solid #e5e7eb; border-radius: 10px;
                    padding: 8px; background: white; font-size: 11px;
                    display: flex; flex-direction: column; justify-content: space-between;
                }
            </style>
        """, unsafe_allow_html=True)

        items_per_page = 6
        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 양 끝 화살표 + 중앙 카드 배치
        cols = st.columns([1, 10, 1])

        with cols[0]:
            if st.button("◀◀"): st.session_state.current_page = 0; st.rerun()
            if st.button("◀"):
                if st.session_state.current_page > 0: st.session_state.current_page -= 1; st.rerun()

        with cols[1]:
            st.markdown('<div class="cards-container">', unsafe_allow_html=True)
            start = st.session_state.current_page * items_per_page
            page_games = game_data_list[start:start + items_per_page]
            
            for game in page_games:
                # 카드와 상세보기 기능을 하나로 묶음
                st.markdown(f"""
                    <div class="card-box">
                        <div style="color:#6b7280;">종료</div>
                        <div style="display:flex; justify-content:space-between; font-weight:bold;"><span>{game.get('away_name', 'AWY')}</span><span>{game.get('away_score', 0)}</span></div>
                        <div style="display:flex; justify-content:space-between;"><span>{game.get('home_name', 'HOM')}</span><span>{game.get('home_score', 0)}</span></div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with cols[2]:
            if st.button("▶"): st.session_state.current_page += 1; st.rerun()
            if st.button("▶▶"): st.session_state.current_page = 99; st.rerun() # 마지막 페이지 로직
