import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        items_per_page = 6
        total_pages = max(1, (len(game_data_list) + items_per_page - 1) // items_per_page)

        if 'current_page' not in st.session_state or st.session_state.current_page >= total_pages:
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

        # 카드 배치 (6개 칼럼 고정)
        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 안전하게 값 가져오기
                    time = str(game.get('game_time', 'TBA'))
                    away = str(game.get('away_name', 'TBA'))
                    home = str(game.get('home_name', 'TBA'))
                    a_score = game.get('away_score', 0)
                    h_score = game.get('home_score', 0)
                    
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:12px; padding:10px; text-align:center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height:120px;">
                            <div style="color:#6b7280; font-size:11px; font-weight:bold; margin-bottom:5px;">{time}</div>
                            <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:13px;">
                                <span>{away}</span> <span style="color:{'red' if a_score > h_score else 'black'};">{a_score}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:13px;">
                                <span>{home}</span> <span style="color:{'red' if h_score > a_score else 'black'};">{h_score}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")
