import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 테두리 및 구분감을 강조한 스타일 적용
        st.markdown("""
            <style>
                .navbar-wrapper { 
                    display: flex !important; 
                    flex-direction: row !important; 
                    align-items: center !important; 
                    justify-content: center !important; 
                    gap: 12px !important; 
                    width: 100% !important; 
                    flex-wrap: nowrap !important;
                    padding: 16px 0;
                }
                .fixed-card { 
                    width: 150px !important; 
                    height: 100px !important; 
                    min-width: 150px !important; 
                    background-color: var(--bg-elevated);
                    /* 테두리 명확화: 1px 실선 적용 */
                    border: 1px solid var(--border-default) !important; 
                    border-radius: var(--radius-lg);
                    /* 구분감을 위한 그림자 */
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    flex-shrink: 0;
                    transition: all 0.2s ease;
                }
                .fixed-card:hover {
                    border-color: var(--brand) !important; /* 호버 시 브랜드 컬러로 강조 */
                    box-shadow: var(--card-shadow-hover);
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        st.markdown('<div class="navbar-wrapper">', unsafe_allow_html=True)
        
        if st.button("◀", key="prev"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()

        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for game in page_games:
            st.markdown(f"""
                <div class="fixed-card">
                    <div style="font-size: 10px; color: var(--text-muted);">{game.get('display_date', '')}</div>
                    <div style="font-weight: bold; margin: 4px 0; font-size: 12px;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                    <div style="font-size: 12px; color: var(--text-secondary);">{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                </div>
            """, unsafe_allow_html=True)

        if st.button("▶", key="next"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
