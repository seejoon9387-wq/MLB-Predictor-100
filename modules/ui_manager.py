import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list, on_card_click):
        st.markdown("""
            <style>
                .custom-card { width: 100%; height: 160px; border: 2px solid #d9ded5; border-radius: 12px; background-color: #fcfcf8; display: flex; flex-direction: column; justify-content: center; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; }
                .text-team { font-weight: 800; font-size: 14px; color: #111827; }
                .text-score { font-weight: 900; font-size: 18px; color: #fe7701; }
            </style>
        """, unsafe_allow_html=True)

        start = st.session_state.get('current_page', 0) * 6
        page_games = game_data_list[start:start + 6]
        
        # 6개의 컬럼으로 카드를 명확하게 나눕니다.
        cols = st.columns(6)
        for i, col in enumerate(cols):
            with col:
                if i < len(page_games):
                    game = page_games[i]
                    # 카드 클릭 시 상세 정보 호출
                    if st.button("상세보기", key=f"btn_{i}"):
                        on_card_click(game)
                    st.markdown(f"""
                        <div class="custom-card">
                            <div class="text-team">{game['away_name']}</div>
                            <div class="text-score">{game['away_score']} : {game['home_score']}</div>
                            <div class="text-team">{game['home_name']}</div>
                        </div>
                    """, unsafe_allow_html=True)
