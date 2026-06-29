import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list, on_card_click):
        # 디자인 스타일
        st.markdown("""
            <style>
                .game-card { border: 2px solid #d9ded5; border-radius: 10px; padding: 10px; text-align: center; background-color: #fcfcf8; height: 160px; display: flex; flex-direction: column; justify-content: center; }
            </style>
        """, unsafe_allow_html=True)

        start = st.session_state.get('current_page', 0) * 6
        page_games = game_data_list[start:start + 6]
        
        # 행 생성 및 6개 컬럼 분할
        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 카드 정보
                    st.markdown(f"""
                        <div class="game-card">
                            <strong>{game.get('away_name', 'AWY')}</strong><br>
                            <h3 style="color: #fe7701; margin: 5px 0;">{game.get('away_score', 0)} : {game.get('home_score', 0)}</h3>
                            <strong>{game.get('home_name', 'HOM')}</strong>
                        </div>
                    """, unsafe_allow_html=True)
                    # 상세보기 버튼
                    if st.button("상세보기", key=f"btn_{i}"):
                        on_card_click(game)
                else:
                    st.write("")
