import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 디자인 시스템(CSS 변수)과 강제 일렬 배치를 결합한 스타일
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
                    border: 1px solid var(--border-default);
                    border-radius: var(--radius-lg);
                    box-shadow: var(--card-shadow);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    flex-shrink: 0;
                    cursor: pointer;
                    transition: box-shadow var(--default-transition-duration) var(--default-transition-timing-function);
                }
                .fixed-card:hover {
                    box-shadow: var(--card-shadow-hover);
                    border-color: var(--brand-border);
                }
                /* 화살표 버튼 스타일링 */
                .arrow-btn {
                    background: none !important;
                    border: 1px solid var(--border-default) !important;
                    border-radius: var(--radius-md) !important;
                    padding: 8px 12px !important;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        st.markdown('<div class="navbar-wrapper">', unsafe_allow_html=True)
        
        # 화살표 버튼 (클래스 적용)
        if st.button("◀", key="prev"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 카드 배치
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
