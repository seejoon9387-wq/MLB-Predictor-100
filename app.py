import streamlit as st
import statsapi
from datetime import datetime, timedelta
from modules.ui_manager import UIManager

def get_filtered_mlb_data():
    # 1. 미국 날짜 기준으로 오늘과 내일 데이터를 가져옴 (시차 때문에 내일 데이터까지 긁어와야 함)
    today = '2026-06-30'
    tomorrow = '2026-07-01'
    
    raw_data = statsapi.schedule(start_date=today, end_date=tomorrow)
    
    filtered_data = []
    for game in raw_data:
        # 2. 각 게임의 UTC 시간을 KST로 변환
        dt_utc = datetime.strptime(game['game_datetime'], "%Y-%m-%dT%H:%M:%SZ")
        dt_kst = dt_utc + timedelta(hours=9)
        
        # 3. KST 날짜가 6월 30일인 것만 선택!
        if dt_kst.strftime("%Y-%m-%d") == "2026-06-30":
            filtered_data.append(game)
            
    return filtered_data

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ 2026년 6월 30일 한국 시간 기준 경기")
    
    games = get_filtered_mlb_data()
    
    if games:
        UIManager.render_game_navbar(games)
    else:
        st.info("한국 시간 6월 30일 당일에는 예정된 경기가 없습니다.")

if __name__ == "__main__":
    main()
