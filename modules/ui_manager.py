import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 스트림릿의 강제 줄바꿈을 CSS로 완전히 봉쇄합니다.
        st.markdown("""
            <style>
                /* 전체를 감싸는 영역을 flex로 강제 설정 */
                .outer-container { 
                    display: flex !important; 
                    flex-direction: row !important; 
                    align-items: center !important; 
                    justify-content: center !important; 
                    gap: 10px !important; 
                    width: 100% !important;
                }
                /* 모든 버튼을 인라인으로 변환하여 줄바꿈 차단 */
                div.stButton { display: inline-block !important; }
                
                /* 카드 디자인: 고정 폭 */
                .game-card { 
                    width: 120px !important; 
                    height: 90px !important; 
                    border: 1px solid #ccc; 
                    border-radius: 8px; 
                    background: white; 
                    display: flex; 
                    flex-direction: column; 
                    justify-content: center;
                    align-items: center;
                    flex-shrink: 0; 
                    font-size: 10px;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 하나의 div 안에 모든 요소를 넣습니다 (가장 중요)
        st.markdown('<div class="outer-container">', unsafe_allow_html=True)
        
        if st.button("◀", key="prev"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()

        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for game in page_games:
            st.markdown(f"""
                <div class="game-card">
                    <div style="color:gray;">{game.get('display_date', '')}</div>
                    <div style="font-weight:bold;">{game.get('away_name', 'AWY')}</div>
                    <div>{game.get('home_name', 'HOM')}</div>
                </div>
            """, unsafe_allow_html=True)

        if st.button("▶", key="next"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
