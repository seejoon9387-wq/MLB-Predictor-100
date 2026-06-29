import streamlit as st
from datetime import datetime, timedelta

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
                    
                    # 날짜/시간 변환 로직 (안전한 try-except)
                    try:
                        dt_utc = datetime.strptime(game.get('game_datetime', ''), "%Y-%m-%dT%H:%M:%SZ")
                        dt_kst = dt_utc + timedelta(hours=9)
                        date_val = dt_kst.strftime("%m월 %d일")
                        time_val = dt_kst.strftime("%H:%M")
                    except:
                        date_val, time_val = "날짜 미정", "시간 미정"
                    
                    st.markdown(f"""
                        <div style="background:#f9fafb; border:1px solid #e5e7eb; border-radius:10px; padding:10px; text-align:center; height:180px;">
                            <div style="font-size:12px; font-weight:bold; color:#4b5563;">{date_val}</div>
                            <div style="font-size:14px; font-weight:bold; color:#dc2626; margin-bottom:10px;">{time_val}</div>
                            <div style="font-size:13px; font-weight:bold;">{game.get('away_name', 'AWAY')} ({game.get('away_score', 0)})</div>
                            <div style="font-size:13px; font-weight:bold;">{game.get('home_name', 'HOME')} ({game.get('home_score', 0)})</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")
