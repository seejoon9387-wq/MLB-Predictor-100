import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 스타일 정의 (보내주신 디자인과 동일)
        st.markdown("""
            <style>
                .nav-container { display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 20px; }
                .game-card-styled { 
                    border: 1px solid #e5e7eb; border-radius: 12px; padding: 12px 16px; 
                    background: white; width: 140px; height: 100px;
                    display: flex; flex-direction: column; justify-content: space-between;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1); cursor: pointer;
                }
                .card-header { font-size: 10px; color: #6b7280; margin-bottom: 4px; }
                .team-row { display: flex; justify-content: space-between; font-size: 13px; font-weight: 600; }
            </style>
        """, unsafe_allow_html=True)

        # 페이지 처리
        items_per_page = 6
        start = st.session_state.get('current_page', 0) * items_per_page
        page_games = game_data_list[start:start + items_per_page]

        # 2. 버튼 + 카드 한 줄로 배치
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        
        # 이전 버튼
        if st.button("◀"):
            if st.session_state.get('current_page', 0) > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 카드 루프
        for game in page_games:
            # 상세보기 클릭 처리
            if st.button(label="", key=f"btn_{game.get('game_id')}"):
                st.session_state.selected_game_id = game.get('game_id')
                st.rerun()
            
            # HTML 카드 디자인
            st.markdown(f"""
                <div class="game-card-styled">
                    <div class="card-header">{game.get('display_date', '종료')}</div>
                    <div class="team-row"><span>{game.get('away_name', 'AWY')}</span><span>{game.get('away_score', 0)}</span></div>
                    <div class="team-row"><span>{game.get('home_name', 'HOM')}</span><span>{game.get('home_score', 0)}</span></div>
                </div>
            """, unsafe_allow_html=True)

        # 다음 버튼
        if st.button("▶"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
