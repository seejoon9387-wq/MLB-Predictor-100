import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 카드 높이를 150px로 강제 고정하는 CSS 추가
        st.markdown("""
            <style>
                [data-testid="stVerticalBlockBorderWrapper"] {
                    min-height: 150px !important;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 1. 상단 레이아웃
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
                    # st.container에 border=True를 적용하면 
                    # 위에서 설정한 CSS(150px)가 적용됩니다.
                    with st.container(border=True):
                        st.markdown(f"<div style='text-align:center;'>", unsafe_allow_html=True)
                        st.markdown(f"**{game.get('away_name', 'AWY')}**")
                        st.write(f"{game.get('away_score', 0)} : {game.get('home_score', 0)}")
                        st.markdown(f"**{game.get('home_name', 'HOM')}**")
                        st.caption(game.get('display_date', ''))
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.write("") 

        st.caption(f"페이지 {st.session_state.current_page + 1}")
