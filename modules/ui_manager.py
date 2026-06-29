import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        items_per_page = 6
        total_pages = max(1, (len(game_data_list) + items_per_page - 1) // items_per_page)

        if 'current_page' not in st.session_state or st.session_state.current_page >= total_pages:
            st.session_state.current_page = 0

        # 버튼 및 페이지 표시 영역
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

        start = st.session_state.get('current_page', 0) * items_per_page
        end = min(start + items_per_page, len(game_data_list))
        page_games = game_data_list[start:end]

        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    date_val = game.get('display_date', '--/--')
                    time_val = game.get('display_time', '--:--')
                    away = game.get('away_name', 'AWAY')
                    home = game.get('home_name', 'HOME')
                    a_score = game.get('away_score', 0)
                    h_score = game.get('home_score', 0)
                    
                    # 가독성 최적화 HTML
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #e5e7eb; border-radius:16px; padding:12px; text-align:center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); height:190px; display:flex; flex-direction:column; justify-content:center;">
                            <div style="font-size:11px; color:#6b7280; font-weight:600; letter-spacing:0.05em;">{date_val}</div>
                            <div style="font-size:18px; color:#1f2937; font-weight:800; margin-bottom:12px;">{time_val}</div>
                            <div style="display:flex; justify-content:space-between; align-items:center; margin:4px 0; font-size:14px; font-weight:700;">
                                <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:70%;">{away}</span>
                                <span style="color:#ef4444;">{a_score}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; margin:4px 0; font-size:14px; font-weight:700;">
                                <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:70%;">{home}</span>
                                <span style="color:#ef4444;">{h_score}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")
