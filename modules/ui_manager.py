import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 가독성을 위한 스타일 (카드 크기 및 폰트 확대)
        st.markdown("""
            <style>
                .custom-card {
                    width: 100% !important;
                    height: 180px !important; /* 높이 확대 */
                    border: 2px solid #d9ded5 !important;
                    border-radius: 12px !important;
                    background-color: #fcfcf8;
                    display: flex !important;
                    flex-direction: column !important;
                    justify-content: center !important;
                    align-items: center !important;
                    text-align: center !important;
                    overflow: hidden !important;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
                }
                .card-wrapper { padding: 5px; }
                .text-date { font-size: 13px !important; color: #697465 !important; margin-bottom: 8px; }
                .text-team { font-weight: 800 !important; font-size: 16px !important; margin: 2px 0; color: #111827; }
                .text-score { font-weight: 900 !important; font-size: 20px !important; margin: 4px 0; color: #fe7701; }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 상단 화살표
        col1, col2, col3 = st.columns([1, 10, 1])
        with col1:
            if st.button("◀", key="p"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
        with col3:
            if st.button("▶", key="n"):
                st.session_state.current_page += 1
                st.rerun()

        # 3. 카드 레이아웃
        card_cols = st.columns(6)
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for i, col in enumerate(card_cols):
            with col:
                if i < len(page_games):
                    game = page_games[i]
                    # HTML 내부 텍스트에 클래스 적용으로 가독성 개선
                    st.markdown(f"""
                        <div class="card-wrapper">
                            <div class="custom-card">
                                <div class="text-date">{game.get('display_date', '')}</div>
                                <div class="text-team">{game.get('away_name', 'AWY')}</div>
                                <div class="text-score">{game.get('away_score', 0)} : {game.get('home_score', 0)}</div>
                                <div class="text-team">{game.get('home_name', 'HOM')}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")
