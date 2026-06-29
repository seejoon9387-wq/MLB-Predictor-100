import streamlit as st
from datetime import datetime, timedelta

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        items_per_page = 6
        total_pages = max(1, (len(game_data_list) + items_per_page - 1) // items_per_page)

        if 'current_page' not in st.session_state or st.session_state.current_page >= total_pages:
            st.session_state.current_page = 0

        # ... (버튼 로직 생략) ...

        start = st.session_state.get('current_page', 0) * items_per_page
        end = min(start + items_per_page, len(game_data_list))
        page_games = game_data_list[start:end]

        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    
                    # 한국 시간 변환
                    iso_time = game.get('game_datetime', '')
                    if iso_time:
                        dt_utc = datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%SZ")
                        dt_kst = dt_utc + timedelta(hours=9)
                        date_str = dt_kst.strftime("%m월 %d일") # 한국 날짜 형식
                        time_str = dt_kst.strftime("%H:%M")     # 한국 시간 형식
                    else:
                        date_str, time_str = "날짜 확인", "시간 미정"
                    
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:10px; padding:10px; text-align:center; height:180px;">
                            <div style="font-size:12px; font-weight:bold; color:#4b5563;">{date_str}</div>
                            <div style="font-size:14px; font-weight:bold; color:#dc2626; margin-bottom:10px;">{time_str}</div>
                            <div style="font-size:13px; font-weight:bold;">{game.get('away_name', 'AWAY')}: {game.get('away_score', 0)}</div>
                            <div style="font-size:13px; font-weight:bold;">{game.get('home_name', 'HOME')}: {game.get('home_score', 0)}</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")
