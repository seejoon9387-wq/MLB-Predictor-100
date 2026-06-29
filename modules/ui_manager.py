import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 카드 높이를 160px로 완벽히 고정하는 CSS
        st.markdown("""
            <style>
                /* border=True를 적용한 모든 컨테이너의 높이를 160px로 강제 고정 */
                [data-testid="stVerticalBlockBorderWrapper"] {
                    height: 160px !important;
                    min-height: 160px !important;
                    overflow: hidden !important; /* 내용이 넘쳐도 크기 유지 */
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 1. 상단 화살표
        col_nav_left, col_nav_center, col_nav_right = st.columns([1, 8, 1])
        with col_nav_left:
            if st.button("◀ 이전"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
        with col_nav_right:
            if st.button("다음 ▶"):
                st.session_state.current_page += 1
                st.rerun()

        # 2. 카드 레이아웃
        card_cols = st.columns(6)
        
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for i, col in enumerate(card_cols):
            with col:
                if i < len(page_games):
                    game = page_games[i]
                    # border=True를 적용하여 카드 형태 생성
                    with st.container(border=True):
                        # 카드 내부를 중앙 정렬로 배치
                        st.markdown(f"""
                            <div style='text-align:center; display:flex; flex-direction:column; justify-content:center; height:100%;'>
                                <div style='font-size:0.8em; font-weight:bold;'>{game.get('away_name', 'AWY')}</div>
                                <div style='font-size:1.1em; font-weight:bold; margin: 5px 0;'>
                                    {game.get('away_score', 0)} : {game.get('home_score', 0)}
                                </div>
                                <div style='font-size:0.8em; font-weight:bold;'>{game.get('home_name', 'HOM')}</div>
                                <div style='font-size:0.7em; color:gray; margin-top:5px;'>{game.get('display_date', '')}</div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    # 데이터가 없을 때 빈 카드도 높이를 맞춤
                    with st.container(border=True):
                        st.write("")
