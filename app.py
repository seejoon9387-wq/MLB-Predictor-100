import streamlit as st
from modules.ui_manager import UIManager

# @st.cache_data(ttl=0)을 사용하면 함수를 호출할 때마다 캐시를 무효화하고 새로 실행합니다.
@st.cache_data(ttl=0)
def fetch_mlb_live_data():
    """
    이제 이 함수는 호출될 때마다 무조건 새로 실행됩니다.
    여기에 나중에 API 연결 코드를 넣으시면 됩니다.
    """
    # 테스트용: 실시간성 확인을 위해 데이터에 변화를 줄 수 있는 구조로 변경
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
    
    # 업데이트 버튼
    if st.button("🔄 실시간 데이터 업데이트"):
        # 버튼을 누르면 캐시가 초기화되고 main()이 다시 실행되면서 새로운 데이터를 불러옴
        st.cache_data.clear() 
        st.rerun()
        
    games = fetch_mlb_live_data()
    UIManager.render_game_navbar(games)
    
if __name__ == "__main__":
    main()
