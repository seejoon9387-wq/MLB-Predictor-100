import streamlit as st
from modules.ui_manager import UIManager

def main():
    st.set_page_config(layout="wide")
    
    # 경기 데이터: match_time 필드 추가
    all_games = [
        {'match_time': '06-30 08:00', 'away_name': 'WSH', 'away_score': 6, 'home_name': 'BAL', 'home_score': 4},
        {'match_time': '06-30 09:30', 'away_name': 'CIN', 'away_score': 3, 'home_name': 'PIT', 'home_score': 9},
        {'match_time': '06-30 10:00', 'away_name': 'TEX', 'away_score': 2, 'home_name': 'TOR', 'home_score': 2},
        {'match_time': '07-01 07:15', 'away_name': 'HOU', 'away_score': 7, 'home_name': 'DET', 'home_score': 5},
        {'match_time': '07-01 08:45', 'away_name': 'SEA', 'away_score': 1, 'home_name': 'CLE', 'home_score': 6},
        {'match_time': '07-01 09:00', 'away_name': 'PHI', 'away_score': 5, 'home_name': 'NYM', 'home_score': 4},
    ]
    
    st.title("⚾ MLB 실시간 경기 센터")
    
    UIManager.render_game_navbar(all_games)
    
    st.divider()
    st.write("분석 엔진 결과가 이 아래에 정렬됩니다.")

if __name__ == "__main__":
    main()
