import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list, on_card_click):
        st.markdown("""
            <style>
                .grid-container { display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; width: 100%; margin-top: 20px; }
                .card-parent { position: relative; width: 100%; height: 180px; }
                .card-button { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; z-index: 10; cursor: pointer; }
                .custom-card { width: 100%; height: 180px; border: 2px solid #d9ded5; border-radius: 12px; background-color: #fcfcf8; display: flex; flex-direction: column; justify-content: center; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                .team-text { font-weight: 800; font-size: 14px; }
                .score-text { font-weight: 900; font-size: 18px; color: #fe7701; }
            </style>
        """, unsafe_allow_html=True)

        start = st.session_state.get('current_page', 0) * 6
        page_games = game_data_list[start:start + 6]
        
        # Grid 레이아웃 시작
        st.markdown('<div class="grid-container">', unsafe_allow_html=True)
        for i, game in enumerate(page_games):
            # 카드를 별도의 영역으로 확실히 정의
            if st.button(" ", key=f"btn_{i}"):
                on_card_click(game)
            st.markdown(f"""
                <div class="custom-card">
                    <div class="team-text">{game['away_name']}</div>
                    <div class="score-text">{game['away_score']} : {game['home_score']}</div>
                    <div class="team-text">{game['home_name']}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
