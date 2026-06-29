import streamlit as st
import requests  # 외부 데이터를 불러오기 위한 라이브러리
from modules.ui_manager import UIManager

@st.cache_data(ttl=60) # 60초마다 캐시 갱신
def fetch_mlb_live_data():
    """
    실제 MLB 실시간 API를 호출하는 로직입니다.
    """
    try:
        # 여기에 MLB 실시간 경기 정보를 제공하는 API URL을 입력합니다.
        # 예시: response = requests.get("https://api.mlb.com/...")
        # 응답 받은 데이터를 리스트 형태로 가공해서 리턴합니다.
        
        # 지금은 API가 없으므로 사용자님이 이해하기 쉽게 
        # API를 호출하는 '구조'만 보여드립니다.
        data = [
            {'match_time': '07:15', 'away_name': 'HOU', 'away_score': 7, 'home_name': 'DET', 'home_score': 5},
            # ... API에서 받아온 실시간 데이터 ...
        ]
        return data
    except Exception as e:
        return []

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ 2026년 6월 30일 MLB 실시간 경기")
    
    # 데이터 새로고침 버튼
    if st.button("🔄 실시간 데이터 업데이트"):
        st.cache_data.clear()  # 캐시를 지워서 강제로 다시 읽게 함
        st.rerun()
        
    games = fetch_mlb_live_data()
    
    if games:
        UIManager.render_game_navbar(games)
    else:
        st.error("데이터를 불러오지 못했습니다. API 연결을 확인해주세요.")
    
if __name__ == "__main__":
    main()
