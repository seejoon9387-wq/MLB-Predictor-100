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

        # 카드 영역: 6개 칼럼 생성
        cols = st.columns(items_per_page)
        for i in range(items_per_page):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 승패 컬러 결정
                    a_color = "red" if game['away_score'] > game['home_score'] else "black"
                    h_color = "red" if game['home_score'] > game['away_score'] else "black"
                    
                    # 카드 테두리 및 디자인 (Streamlit 스타일)
                    with st.container(border=True):
                        st.caption(game['match_time'])
                        # 점수 표시
                        col_away, col_home = st.columns(2)
                        col_away.write(f"{game['away_name']}")
                        col_away.markdown(f":red[{game['away_score']}]" if a_color == "red" else f"{game['away_score']}")
                        col_home.write(f"{game['home_name']}")
                        col_home.markdown(f":red[{game['home_score']}]" if h_color == "red" else f"{game['home_score']}")
                else:
                    # 데이터가 없으면 빈 공간
                    st.empty()
