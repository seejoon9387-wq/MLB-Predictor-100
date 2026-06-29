import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 1. 상단 레이아웃 (화살표 버튼 배치)
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

        # 2. 카드 레이아웃 (6개 컬럼으로 고정)
        # 카드 6개를 담을 6개 컬럼 생성
        card_cols = st.columns(6)
        
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for i, col in enumerate(card_cols):
            with col:
                if i < len(page_games):
                    game = page_games[i]
                    # 버튼처럼 동작하게 만들고 싶다면 st.button을 사용해도 되지만, 
                    # 레이아웃을 위해 st.container를 사용
                    with st.container(border=True):
                        st.markdown(f"**{game.get('away_name')}**")
                        st.write(f"{game.get('away_score')} : {game.get('home_score')}")
                        st.markdown(f"**{game.get('home_name')}**")
                        st.caption(game.get('display_date', ''))
                else:
                    st.write("") # 빈 컬럼 유지

        # 3. 페이지 정보 표시 (편의성)
        st.caption(f"페이지 {st.session_state.current_page + 1}")
