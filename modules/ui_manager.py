import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 완벽한 일렬 배치를 위한 CSS 정의
        st.markdown("""
            <style>
                .nav-full-container { display: flex; align-items: center; justify-content: center; gap: 20px; width: 100%; margin-top: 10px; }
                .card-row { display: flex; flex-direction: row; gap: 10px; align-items: center; }
                .game-card { 
                    width: 140px; height: 90px; border: 1px solid #ddd; border-radius: 8px; 
                    padding: 8px; background: white; flex-shrink: 0; font-size: 11px;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]

        # 2. 하나의 div 컨테이너 안에 화살표와 카드를 모두 배치
        st.markdown('<div class="nav-full-container">', unsafe_allow_html=True)
        
        # 이전 화살표 (HTML 버튼 클릭 처리)
        if st.button("◀", key="prev_btn"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 카드 6개 배치
        st.markdown('<div class="card-row">', unsafe_allow_html=True)
        for game in page_games:
            st.markdown(f"""
                <div class="game-card">
                    <div style="color:gray;">{game.get('display_date', '')}</div>
                    <div style="font-weight:bold;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                    <div>{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 다음 화살표
        if st.button("▶", key="next_btn"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
