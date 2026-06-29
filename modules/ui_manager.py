import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 화살표 전용 상단 컨테이너와 하단 카드 컨테이너 분리
        st.markdown("""
            <style>
                /* 화살표를 양 끝으로 벌리는 컨테이너 */
                .arrow-container { 
                    display: flex !important; 
                    justify-content: space-between !important; 
                    width: 100% !important; 
                    margin-bottom: 10px;
                }
                /* 카드 배치 컨테이너 */
                .card-container { 
                    display: flex !important; 
                    justify-content: center !important; 
                    gap: 15px !important; 
                    flex-wrap: nowrap !important;
                }
                .fixed-card { 
                    width: 150px !important; height: 100px !important; 
                    border: 2px solid var(--border-default) !important; 
                    border-radius: var(--radius-lg);
                    box-shadow: 0 4px 10px rgba(0,0,0,0.15) !important;
                    display: flex; flex-direction: column; justify-content: center; align-items: center;
                    flex-shrink: 0; background-color: var(--bg-elevated);
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 화살표 레이아웃 (최상단, 양 끝 배치)
        st.markdown('<div class="arrow-container">', unsafe_allow_html=True)
        
        # 왼쪽 화살표 (이 컨테이너 안에서는 flex로 정렬됨)
        if st.button("◀", key="prev_top"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 오른쪽 화살표
        if st.button("▶", key="next_top"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 3. 카드 레이아웃 (화살표 아래에 별도 배치)
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
