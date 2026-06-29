import streamlit as st
from modules.ui_manager import UIManager

def fetch_mlb_live_data():
    # 여기서 데이터를 가져옵니다. 
    # 나중에 API로 교체하면 버튼 누를 때마다 최신 값을 가져오게 됩니다.
    return [
        {'match_time': '07:15', 'away_name': 'HOU', 'away_score': 7, 'home_name': 'DET', 'home_score': 5},
        {'match_time': '08:00', 'away_name': 'WSH', 'away_score': 6, 'home_name': 'BAL', 'home_score': 4},
        # ... 데이터 리스트 ...
    ]

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ 2026년 6월 30일 MLB 실시간 경기")
    
    # 실시간 업데이트 버튼
    if st.button("🔄 실시간 데이터 업데이트"):
        st.toast("최신 정보를 불러오는 중입니다...")
        st.rerun() # 전체 화면을 다시 그려서 데이터를 새로 불러옴
        
    games = fetch_mlb_live_data()
    UIManager.render_game_navbar(games)
    
if __name__ == "__main__":
    main()
