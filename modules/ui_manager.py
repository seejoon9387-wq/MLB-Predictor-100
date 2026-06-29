import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list, on_card_click):
        st.markdown("""
            <style>
                .custom-card { border: 2px solid #d9ded5; border-radius: 12px; background-color: #fcfcf8; padding: 10px; text-align: center; height: 160px; display: flex; flex-direction: column; justify-content: center; }
                .text-team { font-weight: 800; font-size: 14px; }
                .text-score { font-weight: 900; font-size: 18px; color: #fe7701; }
            </style>
        """, unsafe_allow_html=True)

        start = st.session_state.get('current_page', 0) * 6
        page_games = game_data_list[start:start + 6]
        
        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                with st.container(height=240):
                    if i < len(page_games):
                        game = page_games[i]
                        # 버튼을 누르면 상세 정보를 로딩
                        if st.button("상세보기", key=f"btn_{i}"):
                            on_card_click(game)
                        # 데이터를 안전하게 가져오기 (get 사용)
                        st.markdown(f"""
                            <div class="custom-card">
                                <div class="text-team">{game.get('away_name', 'AWY')}</div>
                                <div class="text-score">{game.get('away_score', 0)} : {game.get('home_score', 0)}</div>
                                <div class="text-team">{game.get('home_name', 'HOM')}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.write("")
