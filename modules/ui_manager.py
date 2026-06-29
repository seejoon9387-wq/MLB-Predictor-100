import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 완벽한 일렬 배치를 위한 CSS
        st.markdown("""
            <style>
                .nav-container { 
                    display: flex; align-items: center; justify-content: space-between; 
                    width: 100%; padding: 20px 0; 
                }
                .cards-container { 
                    display: flex; gap: 15px; justify-content: center; flex: 1; 
                }
                .card-box { 
                    width: 150px; height: 90px; border: 1px solid #ddd; 
                    border-radius: 8px; padding: 10px; background: white;
                    display: flex; flex-direction: column; justify-content: space-between;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 레이아웃 렌더링
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        
        # 왼쪽 화살표 (st.button 대신 CSS 스타일이 적용된 클릭 요소)
        if st.button("◀", key="prev"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 카드 영역
        st.markdown('<div class="cards-container">', unsafe_allow_html=True)
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for game in page_games:
            st.markdown(f"""
                <div class="card-box">
                    <div style="font-size:9px; color:gray;">{game.get('display_date', '')}</div>
                    <div style="font-size:12px; font-weight:bold;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                    <div style="font-size:12px;">{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 오른쪽 화살표
        if st.button("▶", key="next"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
