import streamlit as st
from modules.ui_manager import UIManager

# 테스트용 데이터 함수 (실제 API 연동 시 이 부분만 교체하면 됩니다)
def fetch_mlb_live_data():
    # 7개의 데이터를 항상 반환하도록 구성
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
    
    # 1. 데이터 업데이트 버튼
    if st.button("🔄 실시간 데이터 업데이트"):
        st.cache_data.clear() # 캐시 삭제
        st.rerun() # 화면 새로고침
        
    # 2. 데이터 가져오기 (세션 상태에 저장하여 유지)
    if 'game_data' not in st.session_state:
        st.session_state.game_data = fetch_mlb_live_data()
    
    # 3. UI 렌더링
    UIManager.render_game_navbar(st.session_state.game_data)
    
if __name__ == "__main__":
    main()
