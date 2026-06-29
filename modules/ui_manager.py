import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 스타일 정의 (보내주신 디자인과 유사하게 조정)
        st.markdown("""
            <style>
                .game-card-custom { 
                    border: 1px solid #d1d5db; 
                    border-radius: 8px; 
                    padding: 8px 12px; 
                    background: #ffffff; 
                    display: flex; 
                    flex-direction: column; 
                    gap: 4px; 
                    width: 100%;
                    max-width: 150px; /* 고정 너비로 균일하게 */
                    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                }
                .status-txt { font-size: 9px; color: #6b7280; text-transform: uppercase; }
                .score-row { display: flex; justify-content: space-between; align-items: center; font-size: 11px; }
            </style>
        """, unsafe_allow_html=True)

        # 페이지 처리
        items_per_page = 6
        start = st.session_state.get('current_page', 0) * items_per_page
        page_games = game_data_list[start:start + items_per_page]

        # 버튼 및 카드 배치
        cols = st.columns(6) 
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # HTML 직접 삽입으로 디자인 정밀 구현
                    st.markdown(f"""
                        <div class="game-card-custom">
                            <span class="status-txt">{game.get('display_date', '종료')}</span>
                            <div class="score-row">
                                <b>{game.get('away_name', 'AWY')}</b>
                                <span>{game.get('away_score', 0)}</span>
                            </div>
                            <div class="score-row">
                                <span>{game.get('home_name', 'HOM')}</span>
                                <span>{game.get('home_score', 0)}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("상세보기", key=f"btn_{game.get('game_id', i)}"):
                        st.session_state.selected_game_id = game.get('game_id')
                        st.rerun()
                else:
                    st.write("")
