import streamlit as st
from datetime import datetime, timedelta

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # (페이지 이동 로직은 동일)
        
        def convert_to_kst(iso_time_str):
            try:
                # 1. UTC 시간 문자열을 datetime 객체로 변환
                # Z(UTC)를 명시적으로 처리
                dt_utc = datetime.strptime(iso_time_str, "%Y-%m-%dT%H:%M:%SZ")
                
                # 2. 한국 시간(KST)으로 9시간 더하기
                dt_kst = dt_utc + timedelta(hours=9)
                
                # 3. KST 기준으로 날짜와 시간 분리
                return dt_kst.strftime("%m/%d"), dt_kst.strftime("%H:%M")
            except:
                return "날짜 오류", "시간 오류"

        # (페이지 로직 생략 - 이전과 동일)
        # ... (중략) ...
        
        # UI 출력 부분
        # ... (안에서)
        date_val, time_val = convert_to_kst(game.get('game_datetime', ''))
        
        st.markdown(f"""
            <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:12px; padding:10px; text-align:center; height:180px;">
                <div style="color:#111827; font-size:12px; font-weight:bold;">{date_val}</div>
                <div style="color:#dc2626; font-size:14px; font-weight:bold; margin-bottom:8px;">{time_val}</div>
                <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:13px;">
                    <span>{away}</span> <span>{a_score}</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:13px;">
                    <span>{home}</span> <span>{h_score}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
