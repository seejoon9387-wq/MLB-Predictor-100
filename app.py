import streamlit as st
from modules.ui_manager import UIManager

def get_today_games():
    """6월 30일 경기 데이터를 시간순으로 정렬하여 반환"""
    data = [
        {'match_time': '07:15', 'away_name': 'HOU', 'away_score': 7, 'home_name': 'DET', 'home_score': 5},
        {'match_time': '08:00', 'away_name': 'WSH', 'away_score': 6, 'home_name': 'BAL', 'home_score': 4},
        {'match_time': '08:45', 'away_name': 'SEA', 'away_score': 1, 'home_name': 'CLE', 'home_score': 6},
        {'match_time': '09:00', 'away_name': 'PHI', 'away_score': 5, 'home_name': 'NYM', 'home_score': 4},
        {'match_time': '09:30', 'away_name': 'CIN', 'away_score': 3, 'home_name': 'PIT', 'home_score': 9},
        {'match_time': '10:00', 'away_name': 'TEX', 'away_score': 2, 'home_name': 'TOR', 'home_score': 2},
        # ... 추가 경기들
    ]
    # 시간 기준으로 정렬
    return sorted(data, key=lambda x: x['match_time'])

def main():
    st.set_page_config(layout="wide", page_title="MLB 실시간 분석")
    st.title("⚾ 2026년 6월 30일 MLB 경기 현황")
    
    games = get_today_games()
    UIManager.render_game_navbar(games)
    
    st.divider()
    st.write("상세 분석을 위해 경기를 선택하세요.")

if __name__ == "__main__":
    main()
