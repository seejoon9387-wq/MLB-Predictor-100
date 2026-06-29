import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 겹침 방지 핵심 스타일
        st.markdown("""
            <style>
                .nav-container { 
                    display: flex !important; 
                    flex-direction: row !important; 
                    align-items: center !important; 
                    justify-content: center !important; 
                    gap: 5px !important; /* 카드 간격 5px */
                    width: 100% !important;
                }
                .fixed-card { 
                    width: 120px !important; /* 카드를 조금 작게 조정하여 겹침 방지 */
                    height: 100px !important; 
                    border: 1px solid #ccc; 
                    border-radius: 8px; 
                    padding: 5px; 
                    background: white; 
                    text-align: center;
                    flex: 0 0 120px; /* 크기 고정 */
                    font-size: 10px;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 하나의 div로 묶어서 배치 (st.columns 미사용)
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        
        # 화살표 버튼 (inline-block 처리를 위해 st.button 대신 링크나 폼 가능하나, 우선 st.button 유지)
        if st.button("◀", key="prev"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 카드 6개 배치
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for game in page_games:
            st.markdown(f"""
                <div class="fixed-card">
                    <div style="color:gray;">{game.get('display_date', '')}</div>
                    <div style="font-weight:bold; margin-top:5px;">{game.get('away_name', 'AWY')}</div>
                    <div>{game.get('home_name', 'HOM')}</div>
                </div>
            """, unsafe_allow_html=True)

        if st.button("▶", key="next"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
