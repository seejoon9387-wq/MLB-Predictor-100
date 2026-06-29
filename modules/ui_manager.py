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

        # 데이터 계산
        start = st.session_state.current_page * items_per_page
        end = min(start + items_per_page, len(game_data_list))
        page_games = game_data_list[start:end]

        # 카드 영역 - 항상 6개의 칼럼을 고정으로 생성
        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 승패 점수 컬러
                    a_color = "red" if game['away_score'] > game['home_score'] else "black"
                    h_color = "red" if game['home_score'] > game['away_score'] else "black"
                    
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:12px; padding:15px; text-align:center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <div style="color:#6b7280; font-size:12px; font-weight:bold;">{game['match_time']}</div>
                            <div style="display:flex; justify-content:space-between; font-weight:bold;"><span>{game['away_name']}</span> <span style="color:{a_color};">{game['away_score']}</span></div>
                            <div style="display:flex; justify-content:space-between; font-weight:bold;"><span>{game['home_name']}</span> <span style="color:{h_color};">{game['home_score']}</span></div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # 데이터가 없는 칸은 빈 공간으로 유지
                    st.write("")
