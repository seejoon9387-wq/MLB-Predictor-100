import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        items_per_page = 6
        total_pages = (len(game_data_list) + items_per_page - 1) // items_per_page

        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0

        # 버튼 영역
        c1, c2, c3 = st.columns([1, 10, 1])
        with c1:
            if st.button("◀ 이전"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
        with c3:
            if st.button("다음 ▶"):
                if st.session_state.current_page < total_pages - 1:
                    st.session_state.current_page += 1
                    st.rerun()

        # 현재 페이지 데이터
        start = st.session_state.current_page * items_per_page
        end = start + items_per_page
        page_games = game_data_list[start:end]

        # 카드 영역
        cols = st.columns(items_per_page)
        for i in range(items_per_page):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 승패 컬러 로직
                    is_away_win = game['away_score'] > game['home_score']
                    is_home_win = game['home_score'] > game['away_score']
                    
                    with st.container(border=True):
                        st.write(f"**{game['match_time']}**")
                        # 텍스트로 깔끔하게 표시
                        st.write(f"{game['away_name']}: {game['away_score'] if not is_away_win else '🔴' + str(game['away_score'])}")
                        st.write(f"{game['home_name']}: {game['home_score'] if not is_home_win else '🔴' + str(game['home_score'])}")
                else:
                    st.write("")
