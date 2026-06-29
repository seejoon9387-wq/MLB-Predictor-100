import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list, on_card_click):
        st.markdown("""
            <style>
                .custom-card { border: 2px solid #d9ded5; border-radius: 12px; background-color: #fcfcf8; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: 180px; display: flex; flex-direction: column; justify-content: center; }
                .team-text { font-weight: 800; font-size: 14px; margin-bottom: 5px; }
                .score-text { font-weight: 900; font-size: 18px; color: #fe7701; margin-bottom: 5px; }
            </style>
        """, unsafe_allow_html=True)

        start = st.session_state.get('current_page', 0) * 6
        page_games = game_data_list[start:start + 6]
        
        # 6개로 나누고, 각 컬럼마다 컨테이너를 넣어 빈 공간이라도 높이를 유지하게 함
        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                with st.container(height=250): # 높이를 강제로 고정하여 사라짐 방지
                    if i < len(page_games):
                        game = page_games[i]
                        if st.button("보기", key=f"btn_{i}"):
                            on_card_click(game)
                        st.markdown(f"""
                            <div class="custom-card">
                                <div class="team-text">{game['away_name']}</div>
                                <div class="score-text">{game['away_score']} : {game['home_score']}</div>
                                <div class="team-text">{game['home_name']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.write("")
