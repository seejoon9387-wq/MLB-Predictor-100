import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        items_per_page = 6
        total_pages = max(1, (len(game_data_list) + items_per_page - 1) // items_per_page)

        # 페이지 번호가 데이터 범위를 벗어나면 강제로 0으로 조정
        if 'current_page' not in st.session_state or st.session_state.current_page >= total_pages:
            st.session_state.current_page = 0

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

        start = st.session_state.current_page * items_per_page
        end = min(start + items_per_page, len(game_data_list))
        page_games = game_data_list[start:end]

        # 6개 칼럼 고정
        cols = st.columns(items_per_page)
        for i in range(items_per_page):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 카드 디자인
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:12px; padding:15px; text-align:center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <div style="color:#6b7280; font-size:12px; font-weight:bold;">{game['match_time']}</div>
                            <div style="display:flex; justify-content:space-between; font-weight:bold; margin-top:5px;">
                                <span>{game['away_name']}</span> <span style="color:{'red' if game['away_score'] > game['home_score'] else 'black'};">{game['away_score']}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; font-weight:bold;">
                                <span>{game['home_name']}</span> <span style="color:{'red' if game['home_score'] > game['away_score'] else 'black'};">{game['home_score']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("") # 빈 공간
