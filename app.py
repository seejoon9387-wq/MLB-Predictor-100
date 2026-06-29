import streamlit as st
import sys
import os

# 1. 모듈 경로 강제 추가 (에러 방지용)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. 모듈 불러오기
from modules.ui_manager import UIManager

def fetch_mlb_live_data():
    return [
        {'match_time': '07:15', 'away_name': 'HOU', 'away_score': 7, 'home_name': 'DET', 'home_score': 5},
        {'match_time': '08:00', 'away_name': 'WSH', 'away_score': 6, 'home_name': 'BAL', 'home_score': 4},
        {'match_time': '08:45', 'away_name': 'SEA', 'away_score': 1, 'home_name': 'CLE', 'home_score': 6},
        {'match_time': '09:00', 'away_name': 'PHI', 'away_score': 5, 'home_name': 'NYM', 'home_score': 4},
        {'match_time': '09:30', 'away_name': 'CIN', 'away_score': 3, 'home_name': 'PIT', 'home_score': 9},
        {'match_time': '10:00', 'away_name': 'TEX', 'away_score': 2, 'home_name': 'TOR', 'home_score': 2},
        {'match_time': '10:30', 'away_name': 'ATL', 'away_score': 4, 'home_name': 'SFG', 'home_score': 1},
    ]

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ 2026년 6월 30일 MLB 실시간 경기")
    
    if st.button("🔄 실시간 데이터 업데이트"):
        st.cache_data.clear()
        st.rerun()
        
    # 데이터 로드
    games = fetch_mlb_live_data()
    
    # UI 호출
    UIManager.render_game_navbar(games)
    
if __name__ == "__main__":
    main()
