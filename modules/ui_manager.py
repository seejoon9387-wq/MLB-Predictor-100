import streamlit as st
from datetime import datetime, timedelta

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # ... (이전 페이지 로직 동일) ...
        
        # 시간 변환 함수
        def convert_to_kst(iso_time_str):
            try:
                # '2026-06-30T22:35:00Z' 형태를 파싱
                dt = datetime.strptime(iso_time_str, "%Y-%m-%dT%H:%M:%SZ")
                # 9시간을 더해 한국 시간으로 변환
                kst = dt + timedelta(hours=9)
                return kst.strftime("%m/%d %H:%M") # "07/01 07:35" 형태
            except:
                return "시간 미정"

        # (중략 - 페이지 로직은 그대로 사용)
        start = st.session_state.get('current_page', 0) * 6
        end = min(start + 6, len(game_data_list))
        page_games = game_data_list[start:end]

        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 한국 시간 변환 적용
                    time_val = convert_to_kst(game.get('game_datetime', ''))
                    away = game.get('away_name', 'AWAY')
                    home = game.get('home_name', 'HOME')
                    a_score = game.get('away_score', 0)
                    h_score = game.get('home_score', 0)
                    
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:12px; padding:15px; text-align:center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height:190px;">
                            <div style="color:#4b5563; font-size:11px; font-weight:bold; margin-bottom:5px;">{time_val}</div>
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
