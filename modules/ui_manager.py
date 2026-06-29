import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 스타일 설정
        st.markdown("""
            <style>
                /* 화살표 컨테이너: 좌우 끝 배치 */
                .arrow-box { 
                    display: flex !important; 
                    justify-content: space-between !important; 
                    width: 100% !important; 
                    padding: 0 20px !important; 
                    margin-bottom: 20px;
                }
                /* 카드 컨테이너: 중앙 배치 */
                .card-container { 
                    display: flex !important; 
                    justify-content: center !important; 
                    gap: 15px !important; 
                    width: 100% !important;
                }
                .fixed-card { 
                    width: 150px !important; height: 100px !important; 
                    border: 2px solid var(--border-default) !important; 
                    border-radius: var(--radius-lg);
                    background-color: var(--bg-elevated);
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
                    display: flex; flex-direction: column; justify-content: center; align-items: center;
                    flex-shrink: 0;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 화살표 영역 (양 끝 배치)
        st.markdown('<div class="arrow-box">', unsafe_allow_html=True)
        # 컬럼을 쓰지 않고 직접 버튼 배치 (CSS가 먹히도록)
        if st.button("◀", key="prev"):
            st.session_state.current_page = max(0, st.session_state.current_page - 1)
            st.rerun()
        if st.button("▶", key="next"):
            st.session_state.current_page += 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 3. 카드 영역 (다시 나타나도록 복구)
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for game in page_games:
            st.markdown(f"""
                <div class="fixed-card">
                    <div style="font-size: 10px; color: var(--text-muted);">{game.get('display_date', '')}</div>
                    <div style="font-weight: 800; font-size: 13px;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                    <div style="font-size: 13px; color: var(--text-secondary);">{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
