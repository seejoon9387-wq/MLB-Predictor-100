import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 디자인 강제 고정 (카드 크기, 패딩, 여백 완전 통제)
        st.markdown("""
            <style>
                .custom-card {
                    width: 100% !important;
                    height: 140px !important;
                    border: 2px solid #d9ded5 !important;
                    border-radius: 8px !important;
                    background-color: #fcfcf8;
                    display: flex !important;
                    flex-direction: column !important;
                    justify-content: center !important;
                    align-items: center !important;
                    text-align: center !important;
                    overflow: hidden !important;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
                }
                .card-wrapper { padding: 5px; }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 화살표 레이아웃
        col1, col2, col3 = st.columns([1, 10, 1])
        with col1:
            if st.button("◀"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
        with col3:
            if st.button("▶"):
                st.session_state.current_page += 1
                st.rerun()

        # 3. 카드 레이아웃 (columns를 쓰되, 내부는 HTML로 직접 그림)
        card_cols = st.columns(6)
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for i, col in enumerate(card_cols):
            with col:
                if i < len(page_games):
                    game = page_games[i]
                    # st.container 대신 마크다운으로 HTML div를 직접 작성
                    st.markdown(f"""
                        <div class="card-wrapper">
                            <div class="custom-card">
                                <div style="font-size: 10px; color: #697465;">{game.get('display_date', '')}</div>
                                <div style="font-weight: 800; font-size: 13px; margin: 4px 0;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                                <div style="font-size: 13px; color: #3f4a3f;">{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")
