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
                    /* 텍스트 줄들을 카드 전체 높이에서 균등하게 배치 */
                    justify-content: space-around !important; 
                    align-items: center !important;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
                    /* 상하 여백을 추가하여 텍스트가 테두리에 붙지 않게 함 */
                    padding: 10px 0 !important;
                }
                .card-wrapper { padding: 5px; }
                
                /* 각 줄을 flex로 설정하여 텍스트 정렬 */
                .text-row {
                    display: flex !important;
                    justify-content: center !important;
                    align-items: center !important;
                    width: 100% !important;
                    height: 30px !important; /* 줄 높이 */
                    text-align: center !important;
                }
                
                .text-date { font-size: 13px !important; color: #697465 !important; font-weight: 500; }
                .text-team { font-weight: 800 !important; font-size: 15px !important; color: #111827; }
                .text-score { font-weight: 900 !important; font-size: 19px !important; color: #fe7701; }
            </style>
        """, unsafe_allow_html=True)

        # 페이지네이션 상태 관리
        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 상단 네비게이션
        col1, col2, col3 = st.columns([1, 10, 1])
        with col1:
            if st.button("◀", key="p"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
        with col3:
            if st.button("▶", key="n"):
                # 전체 데이터 개수에 따른 페이지 제한 처리 가능 (선택 사항)
                st.session_state.current_page += 1
                st.rerun()

        # 카드 영역
        card_cols = st.columns(6)
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for i, col in enumerate(card_cols):
            with col:
                if i < len(page_games):
                    game = page_games[i]
                    # 카드 내 텍스트 밸런스 배치
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
                    # 데이터가 없는 빈 컬럼은 빈 공간 유지
                    st.write("")
