import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list, on_card_click):
        # 6개의 컬럼으로 구성
        cols = st.columns(6)
        
        start = st.session_state.get('current_page', 0) * 6
        page_games = game_data_list[start:start + 6]
        
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 카드를 먼저 보여주고, 버튼을 아래에 배치
                    st.markdown(f"""
                        <div style="border: 2px solid #d9ded5; border-radius: 10px; padding: 10px; text-align: center; height: 120px;">
                            <strong>{game.get('away_name', 'AWY')}</strong><br>
                            <span style="font-size: 1.2em; color: #fe7701; font-weight: bold;">
                                {game.get('away_score', 0)} : {game.get('home_score', 0)}
                            </span><br>
                            <strong>{game.get('home_name', 'HOM')}</strong>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # 버튼을 카드 아래에 배치
                    if st.button("상세보기", key=f"btn_{i}"):
                        on_card_click(game)
                else:
                    st.write("") # 빈 곳은 공백 처리
