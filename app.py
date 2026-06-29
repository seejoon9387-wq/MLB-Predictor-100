import streamlit as st
from modules.ui_manager import UIManager

def main():
    st.set_page_config(layout="wide")
    
    # 예시: 승패가 반영된 테스트 데이터
    all_games = [
        {'away_name': 'WSH', 'away_score': 6, 'home_name': 'BAL', 'home_score': 4},
        {'away_name': 'CIN', 'away_score': 3, 'home_name': 'PIT', 'home_score': 9},
        {'away_name': 'TEX', 'away_score': 2, 'home_name': 'TOR', 'home_score': 2}, # 무승부 예시
        {'away_name': 'HOU', 'away_score': 7, 'home_name': 'DET', 'home_score': 5},
        {'away_name': 'SEA', 'away_score': 1, 'home_name': 'CLE', 'home_score': 6},
        {'away_name': 'PHI', 'away_score': 5, 'home_name': 'NYM', 'home_score': 4},
    ]
    
    st.title("⚾ MLB 실시간 경기 센터")
    
    # 내비게이션 바 호출
    UIManager.render_game_navbar(all_games)
    
    st.divider()
    st.write("나머지 엔진 데이터가 이 아래에 정렬됩니다.")

if __name__ == "__main__":
    main()
