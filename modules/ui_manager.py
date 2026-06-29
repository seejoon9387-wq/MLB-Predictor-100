import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list, on_card_click):
        st.markdown("""
            <style>
                .custom-card { border: 2px solid #d9ded5; border-radius: 12px; background-color: #fcfcf8; padding: 10px; text-align: center; height: 160px; display: flex; flex-direction: column; justify-content: center; }
            </style>
        """, unsafe_allow_html=True)

        start = st.session_state.get('current_page', 0) * 6
        page_games = game_data_list[start:start + 6]
        
        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                # 카드 유지를 위해 무조건 컨테이너 배치
                with st.container(height=240):
                    if i < len(page_games):
                        game = page_games[i]
                        # 이 버튼이 클릭을 처리합니다.
                        if st.button("상세보기", key=f"btn_{i}"):
                            on_card_click(game)
                        st.markdown(f"""
                            <div class="custom-card">
                                <strong>{game['away_name']}</strong><br>
                                {game['away_score']} : {game['home_score']}<br>
                                <strong>{game['home_name']}</strong>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.write("")
