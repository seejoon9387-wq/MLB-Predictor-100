import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 디자인 강제 고정 (가로 배치 핵심)
        st.markdown("""
            <style>
                /* 네비게이션 전체를 flex로 고정 */
                .fixed-navbar { 
                    display: flex !important; 
                    flex-direction: row !important; 
                    align-items: center !important; 
                    justify-content: center !important; 
                    gap: 15px !important; 
                    flex-wrap: nowrap !important;
                }
                /* 스트림릿 버튼의 block 속성을 강제로 무효화 */
                div.stButton { 
                    display: inline-block !important; 
                    margin: 0 !important; 
                }
                /* 카드 스타일 */
                .game-card { 
                    width: 140px; height: 100px; border: 1px solid #ddd; 
                    border-radius: 8px; padding: 10px; background: white; 
                    flex-shrink: 0; font-size: 11px; text-align: center;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 컨테이너 렌더링
        st.markdown('<div class="fixed-navbar">', unsafe_allow_html=True)
        
        # 왼쪽 화살표
        if st.button("◀", key="prev"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 카드 6개
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for game in page_games:
            st.markdown(f"""
                <div class="game-card">
                    <div style="color:gray;">{game.get('display_date', '')}</div>
                    <div style="font-weight:bold;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                    <div>{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                </div>
            """, unsafe_allow_html=True)

        # 오른쪽 화살표
        if st.button("▶", key="next"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
