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

        start = st.session_state.current_page * items_per_page
        end = min(start + items_per_page, len(game_data_list))
        page_games = game_data_list[start:end]

        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    
                    # 시간 정제: "2026-06-30T22:35:00Z" -> "22:35"
                    raw_time = game.get('game_datetime', 'T')
                    time_val = raw_time.split('T')[1].split(':')[0] + ":" + raw_time.split('T')[1].split(':')[1]
                    
                    away = game.get('away_name', 'AWAY')
                    home = game.get('home_name', 'HOME')
                    a_score = game.get('away_score', 0)
                    h_score = game.get('home_score', 0)
                    status = game.get('status', 'Scheduled')
                    
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:12px; padding:15px; text-align:center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height:190px;">
                            <div style="color:#6b7280; font-size:12px; font-weight:bold;">{time_val}</div>
                            <div style="color:#3b82f6; font-size:10px; margin-bottom:10px;">{status}</div>
                            <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:14px; margin-bottom:5px;">
                                <span>{away}</span> <span>{a_score}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:14px;">
                                <span>{home}</span> <span>{h_score}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")
