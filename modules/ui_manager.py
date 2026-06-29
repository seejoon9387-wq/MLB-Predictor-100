import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 완벽한 1줄 배치를 위한 CSS
        st.markdown("""
            <style>
                .nav-full-container { 
                    display: flex !important; 
                    flex-direction: row !important; 
                    align-items: center !important; 
                    justify-content: center !important; 
                    gap: 15px !important; 
                    width: 100% !important; 
                }
                .card-item { 
                    width: 140px; height: 90px; border: 1px solid #ddd; border-radius: 8px; 
                    padding: 8px; background: white; flex-shrink: 0; font-size: 11px;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 한 줄 컨테이너 시작
        st.markdown('<div class="nav-full-container">', unsafe_allow_html=True)
        
        # 이전 화살표 (st.button 대신 HTML 버튼 클릭 구현을 위한 폼)
        if st.button("◀", key="prev"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 카드 6개
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for game in page_games:
            st.markdown(f"""
                <div class="card-item">
                    <div style="color:gray;">{game.get('display_date', '')}</div>
                    <div style="font-weight:bold;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                    <div>{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                </div>
            """, unsafe_allow_html=True)

        # 다음 화살표
        if st.button("▶", key="next"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
