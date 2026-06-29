import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # [핵심] 화살표와 카드를 가로로 고정하는 스타일
        st.markdown("""
            <style>
                .navbar-container { display: flex; align-items: center; justify-content: center; gap: 15px; width: 100%; margin: 20px 0; }
                .game-card { 
                    width: 140px; height: 90px; border: 1px solid #ddd; border-radius: 8px; 
                    padding: 8px; background: white; flex-shrink: 0; font-size: 11px;
                    display: flex; flex-direction: column; justify-content: space-between;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # [화살표 버튼 로직] st.button 대신 form 사용 (줄바꿈 방지)
        col1, col2, col3 = st.columns([1, 10, 1])
        
        with col1:
            if st.button("◀", key="prev"):
                if st.session_state.current_page > 0: st.session_state.current_page -= 1; st.rerun()

        with col2:
            # 6개 카드 가로 정렬 컨테이너
            st.markdown('<div style="display: flex; gap: 10px; justify-content: center;">', unsafe_allow_html=True)
            start = st.session_state.current_page * 6
            page_games = game_data_list[start:start + 6]
            
            for game in page_games:
                st.markdown(f"""
                    <div class="game-card">
                        <div style="color:gray;">{game.get('display_date', '')}</div>
                        <div style="font-weight:bold;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                        <div>{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            if st.button("▶", key="next"):
                st.session_state.current_page += 1; st.rerun()
