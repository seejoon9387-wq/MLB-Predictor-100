import streamlit as st
from datetime import datetime, timedelta

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # (페이지 이동 로직은 동일)
        
        def convert_to_kst(iso_time_str):
            try:
                # '2026-06-30T22:35:00Z' 파싱
                dt = datetime.strptime(iso_time_str, "%Y-%m-%dT%H:%M:%SZ")
                # KST로 변환 (UTC + 9시간)
                kst = dt + timedelta(hours=9)
                # 날짜와 시간을 분리하여 반환
                return kst.strftime("%m월 %d일"), kst.strftime("%H:%M")
            except:
                return "날짜 미정", "시간 미정"

        # ... (중략: 페이지 계산 로직) ...
        start = st.session_state.get('current_page', 0) * 6
        end = min(start + 6, len(game_data_list))
        page_games = game_data_list[start:end]

        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    date_val, time_val = convert_to_kst(game.get('game_datetime', ''))
                    away = game.get('away_name', 'AWAY')
                    home = game.get('home_name', 'HOME')
                    a_score = game.get('away_score', 0)
                    h_score = game.get('home_score', 0)
                    
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:12px; padding:10px; text-align:center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height:190px;">
                            <div style="color:#374151; font-size:11px; font-weight:bold;">{date_val}</div>
                            <div style="color:#ef4444; font-size:13px; font-weight:bold; margin-bottom:10px;">{time_val}</div>
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
