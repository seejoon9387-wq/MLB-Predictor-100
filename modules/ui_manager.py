import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        items_per_page = 6
        total_pages = max(1, (len(game_data_list) + items_per_page - 1) // items_per_page)

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

        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    
                    # statsapi의 다양한 필드명 가능성을 고려한 데이터 추출
                    # 1. 시간: game_time 또는 game_datetime
                    time_val = game.get('game_time') or game.get('game_datetime') or 'TBA'
                    # 2. 팀명: away_name, home_name
                    away = game.get('away_name', 'AWAY')
                    home = game.get('home_name', 'HOME')
                    # 3. 점수: away_score, home_score
                    a_score = game.get('away_score', 0)
                    h_score = game.get('home_score', 0)
                    
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:12px; padding:10px; text-align:center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height:140px;">
                            <div style="color:#6b7280; font-size:10px; font-weight:bold; margin-bottom:5px;">{time_val}</div>
                            <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:13px; margin-bottom:5px;">
                                <span>{away}</span> <span style="color:{'red' if a_score > h_score else 'black'};">{a_score}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:13px;">
                                <span>{home}</span> <span style="color:{'red' if h_score > a_score else 'black'};">{h_score}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")
