import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 완벽한 일자 배열을 위한 CSS (세로 쌓임 방지)
        st.markdown("""
            <style>
                /* 전체 내비게이션 바를 가로로 강제 정렬 */
                .full-nav { 
                    display: flex; 
                    flex-direction: row; 
                    align-items: center; 
                    justify-content: center; 
                    gap: 10px; 
                    width: 100%;
                }
                /* 카드 디자인 */
                .game-card-inline { 
                    width: 130px; border: 1px solid #ddd; border-radius: 10px; 
                    padding: 8px; background: white; text-align: center;
                    flex-shrink: 0; /* 가로 배열 유지 핵심 */
                }
            </style>
        """, unsafe_allow_html=True)

        items_per_page = 6
        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 메인 컨테이너 시작
        st.markdown('<div class="full-nav">', unsafe_allow_html=True)
        
        # 이전 화살표
        if st.button("◀", key="prev"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 카드 6개 배치
        start = st.session_state.current_page * items_per_page
        page_games = game_data_list[start:start + items_per_page]
        
        for game in page_games:
            # 카드 HTML (가로 배열 유지)
            st.markdown(f"""
                <div class="game-card-inline">
                    <div style="font-size: 9px; color: #888;">{game.get('display_date', '')}</div>
                    <div style="font-size: 11px; font-weight: bold;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                    <div style="font-size: 11px;">{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                </div>
            """, unsafe_allow_html=True)
            # 상세보기 버튼은 이제 카드 아래가 아니라, 스트림릿 제약상 옆에 붙게 됩니다.

        # 다음 화살표
        if st.button("▶", key="next"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
