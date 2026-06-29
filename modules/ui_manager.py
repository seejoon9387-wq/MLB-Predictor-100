import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list, on_refresh_click, on_card_click):
        st.markdown("""
            <style>
                div.stButton > button { background-color: #fe7701 !important; color: white !important; font-weight: bold !important; border-radius: 8px !important; border: none !important; height: 40px !important; width: 100% !important; }
                .custom-card { width: 100% !important; height: 180px !important; border: 2px solid #d9ded5 !important; border-radius: 12px !important; background-color: #fcfcf8; display: flex !important; flex-direction: column !important; justify-content: space-around !important; align-items: center !important; box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important; padding: 10px 0 !important; cursor: pointer; }
                .card-wrapper { padding: 5px; }
                .text-row { display: flex !important; justify-content: center !important; align-items: center !important; width: 100% !important; height: 30px !important; text-align: center !important; }
                .text-date { font-size: 12px !important; color: #697465 !important; font-weight: 500; }
                .text-team { font-weight: 800 !important; font-size: 14px !important; color: #111827; }
                .text-score { font-weight: 900 !important; font-size: 18px !important; color: #fe7701; }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        col_btn, col1, _, col3 = st.columns([2, 0.5, 5, 0.5])
        with col_btn:
            if st.button("🔄 실시간 경기정보"): on_refresh_click()
        with col1:
            if st.button("◀", key="p") and st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()
        with col3:
            if st.button("▶", key="n"):
                st.session_state.current_page += 1
                st.rerun()

        card_cols = st.columns(6)
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for i, col in enumerate(card_cols):
            with col:
                if i < len(page_games):
                    game = page_games[i]
                    # 카드 전체를 버튼으로 감싸 상세정보 호출
                    if st.button(label="상세보기", key=f"card_{i}", help="클릭하여 상세 정보 보기"):
                        on_card_click(game)
                    st.markdown(f"""
                        <div class="card-wrapper">
                            <div class="custom-card">
                                <div class="text-row text-date">{game.get('display_date', '')} {game.get('display_time', '')}</div>
                                <div class="text-row text-team">{game.get('away_name', 'AWY')}</div>
                                <div class="text-row text-score">{game.get('away_score', 0)} : {game.get('home_score', 0)}</div>
                                <div class="text-row text-team">{game.get('home_name', 'HOM')}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
