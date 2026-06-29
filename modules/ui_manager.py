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

        # 현재 페이지 데이터 슬라이싱
        start = st.session_state.current_page * items_per_page
        end = start + items_per_page
        page_games = game_data_list[start:end]

        # 카드 영역
        cols = st.columns(items_per_page)
        
        # 6개 칼럼을 항상 생성하여 크기 고정
        for i in range(items_per_page):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 승리 팀 빨간색 로직
                    away_color = "red" if game['away_score'] > game['home_score'] else "black"
                    home_color = "red" if game['home_score'] > game['away_score'] else "black"
                    
                    # 카드 디자인 (HTML/CSS 사용 - 깔끔함 유지)
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:12px; padding:15px; text-align:center; color:#333333; font-size:14px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <div style="color:#6b7280; font-size:12px; margin-bottom:8px; font-weight:bold;">{game['match_time']}</div>
                            <div style="display:flex; justify-content:space-between; padding:2px 0; font-weight:bold;">
                                <span>{game['away_name']}</span> <span style="color:{away_color};">{game['away_score']}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; padding:2px 0; font-weight:bold;">
                                <span>{game['home_name']}</span> <span style="color:{home_color};">{game['home_score']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # 데이터가 없으면 빈 공간 (카드 크기 유지용)
                    st.write("")
