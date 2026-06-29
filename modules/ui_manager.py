import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 디자인 시스템 변수를 활용한 고정 스타일 적용
        st.markdown("""
            <style>
                /* 전체 영역을 가로로 고정하고 절대 줄바꿈하지 않음 */
                .navbar-wrapper { 
                    display: flex !important; 
                    flex-direction: row !important; 
                    align-items: center !important; 
                    justify-content: center !important; 
                    gap: 10px !important; 
                    width: 100% !important; 
                    flex-wrap: nowrap !important; /* 줄바꿈 금지 */
                    padding: 10px;
                }
                /* 사이트 디자인 시스템을 적용한 카드 스타일 */
                .fixed-card { 
                    width: 140px !important; 
                    height: 100px !important; 
                    min-width: 140px !important; 
                    background-color: var(--bg-elevated);
                    border: 1px solid var(--border-default);
                    border-radius: var(--radius-lg);
                    box-shadow: var(--card-shadow);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    flex-shrink: 0; /* 카드 크기 고정 */
                    font-family: var(--font-sans);
                    color: var(--text-primary);
                    font-size: 11px;
                }
                /* 스트림릿 기본 버튼의 블록 속성 강제 제거 */
                div.stButton { display: inline-block !important; margin: 0 5px; }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 레이아웃 렌더링
        st.markdown('<div class="navbar-wrapper">', unsafe_allow_html=True)
        
        # 이전 버튼
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
                    <div style="color:var(--text-muted);">{game.get('display_date', '')}</div>
                    <div style="font-weight:bold; margin: 4px 0;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                    <div style="color:var(--text-secondary);">{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                </div>
            """, unsafe_allow_html=True)

        # 다음 버튼
        if st.button("▶", key="next"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
