import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 테두리와 그림자를 훨씬 진하고 명확하게 적용
        st.markdown("""
            <style>
                .navbar-wrapper { 
                    display: flex !important; 
                    flex-direction: row !important; 
                    align-items: center !important; 
                    justify-content: center !important; 
                    gap: 15px !important; 
                    width: 100% !important; 
                    flex-wrap: nowrap !important;
                    padding: 20px 0;
                }
                .fixed-card { 
                    width: 150px !important; 
                    height: 100px !important; 
                    min-width: 150px !important; 
                    background-color: var(--bg-elevated);
                    /* 테두리를 2px로 두껍고 진하게 */
                    border: 2px solid var(--border-default) !important; 
                    border-radius: var(--radius-lg);
                    /* 그림자를 훨씬 진하게 (구분감 확보) */
                    box-shadow: 0 4px 10px rgba(0,0,0,0.15) !important;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    flex-shrink: 0;
                    transition: all 0.2s ease;
                }
                .fixed-card:hover {
                    border: 2px solid var(--brand) !important; /* 호버 시 테두리 색상 강조 */
                    box-shadow: 0 8px 20px rgba(254, 119, 1, 0.3) !important;
                }
                /* 화살표 버튼을 더 눈에 띄게 */
                div.stButton > button {
                    border: 2px solid var(--border-default) !important;
                    font-weight: bold !important;
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
                    <div style="font-size: 10px; color: var(--text-muted); font-weight: 600;">{game.get('display_date', '')}</div>
                    <div style="font-weight: 800; margin: 4px 0; font-size: 13px; color: var(--text-primary);">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                    <div style="font-size: 13px; color: var(--text-secondary); font-weight: 600;">{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                </div>
            """, unsafe_allow_html=True)

        if st.button("▶", key="next"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
