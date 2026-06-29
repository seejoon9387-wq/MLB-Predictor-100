import streamlit as st
import sys
import os

# 모듈 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 예외 처리를 강화하여 라이브러리가 없어도 일단 앱이 뜨게 함
try:
    import statsapi
    STATSAPI_AVAILABLE = True
except ImportError:
    STATSAPI_AVAILABLE = False

from modules.ui_manager import UIManager

def fetch_mlb_data():
    if STATSAPI_AVAILABLE:
        try:
            schedule = statsapi.schedule(date='2026-06-30')
            return schedule if schedule else []
        except:
            return []
    else:
        # 라이브러리가 없을 때 테스트 데이터 반환
        return [{'game_time': '07:15', 'away_name': 'HOU', 'away_score': 7, 'home_name': 'DET', 'home_score': 5}]

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ 2026년 6월 30일 MLB 실시간 경기")
    
    if not STATSAPI_AVAILABLE:
        st.warning("경고: 'mlb-statsapi' 라이브러리가 설치되지 않았습니다. requirements.txt를 확인하세요.")

    if st.button("🔄 데이터 새로고침"):
        st.rerun()
        
    games = fetch_mlb_data()
    
    if games:
        UIManager.render_game_navbar(games)
    else:
        st.info("데이터가 없습니다. 날짜를 확인하거나 API 상태를 점검해주세요.")

if __name__ == "__main__":
    main()
