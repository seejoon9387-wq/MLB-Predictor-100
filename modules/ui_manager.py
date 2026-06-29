import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        st.markdown("""
            <style>
                .custom-card {
                    width: 100% !important;
                    height: 180px !important;
                    border: 2px solid #d9ded5 !important;
                    border-radius: 12px !important;
                    background-color: #fcfcf8;
                    display: flex !important;
                    flex-direction: column !important;
                    justify-content: center !important; /* 텍스트 전체 그룹을 중앙 정렬 */
                    align-items: center !important;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
                    padding: 5px 0 !important;
                }
                .card-wrapper { padding: 5px; }
                
                /* 모든 카드 내 텍스트의 고정 높이와 정렬 */
                .text-row {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    width: 100%;
                    height: 35px; /* 모든 줄의 높이를 35px로 고정 -> 수평 정렬 보장 */
                }
                
                .text-date { font-size: 13px !important; color: #697465 !important; font-weight: 500; }
                .text-team { font-weight: 800 !important; font-size: 15px !important; color: #111827; }
                .text-score { font-weight: 900 !important; font-size: 19px !important; color: #fe7701; }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
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

        card_cols = st.columns(6)
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for i, col in enumerate(card_cols):
            with col:
                if i < len(page_games):
                    game = page_games[i]
                    # 각 줄을 .text-row로 감싸 높이를 강제 고정하여 수평 정렬 유지
                    st.markdown(f"""
                        <div class="card-wrapper">
                            <div class="custom-card">
                                <div class="text-row text-date">{game.get('display_date', '')}</div>
                                <div class="text-row text-team">{game.get('away_name', 'AWY')}</div>
                                <div class="text-row text-score">{game.get('away_score', 0)} : {game.get('home_score', 0)}</div>
                                <div class="text-row text-team">{game.get('home_name', 'HOM')}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")
