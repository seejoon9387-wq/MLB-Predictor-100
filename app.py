import streamlit as st
from modules.ui_manager import UIManager

# 이 함수를 나중에 실시간 API(예: requests.get)로 대체하면 됩니다.
def fetch_mlb_live_data():
    """
    현재 날짜 2026년 6월 30일 기준 실시간 경기 데이터를 가져오는 함수
    (나중에 이 부분을 API 호출 로직으로 바꾸시면 됩니다.)
    """
    # 실제로는 여기서 API를 호출합니다. 
    # 데이터가 없으면 빈 리스트를 반환하여 UI 오류를 방지합니다.
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
    st.set_page_config(layout="wide", page_title="MLB 실시간 센터")
    st.title("⚾ 2026년 6월 30일 MLB 실시간 경기")
    
    # 1. 데이터 가져오기
    live_games = fetch_mlb_live_data()
    
    # 2. UI 표시
    if live_games:
        UIManager.render_game_navbar(live_games)
    else:
        st.write("현재 진행 중인 경기가 없습니다.")
    
    st.divider()

if __name__ == "__main__":
    main()
