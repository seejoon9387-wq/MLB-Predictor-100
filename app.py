import streamlit as st
import statsapi 
from modules.ui_manager import UIManager

@st.cache_data(ttl=60)
def fetch_mlb_live_data():
    try:
        # 데이터가 잘 들어오는지 확인하기 위해 시도
        schedule = statsapi.schedule(date='2026-06-30')
        
        # 만약 데이터가 비어있다면, 현재 날짜에 경기가 없다는 뜻입니다.
        if not schedule:
            return []
            
        games = []
        for game in schedule:
            games.append({
                'match_time': game.get('game_time', 'N/A'), 
                'away_name': game.get('away_name', 'TBA'),
                'away_score': game.get('away_score', 0),
                'home_name': game.get('home_name', 'TBA'),
                'home_score': game.get('home_score', 0)
            })
        return games
    except Exception as e:
        # 여기에 어떤 에러가 났는지 출력하게 합니다.
        st.error(f"상세 에러 내용: {e}")
        return []

# (이하 main 함수 동일)
