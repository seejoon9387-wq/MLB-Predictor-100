import streamlit as st
import statsapi
from datetime import datetime, timedelta
from modules.ui_manager import UIManager

def get_filtered_mlb_data():
    # 시차를 고려해 미국 날짜 6월 29일과 30일 데이터를 모두 가져와야 한국 6월 30일 경기가 포함됨
    raw_data = statsapi.schedule(start_date='2026-06-29', end_date='2026-06-30')
    
    filtered_data = []
    for game in raw_data:
        try:
            # UTC 시간을 KST로 변환
            dt_utc = datetime.strptime(game['game_datetime'], "%Y-%m-%dT%H:%M:%SZ")
            dt_kst = dt_utc + timedelta(hours=9)
            
            # KST 날짜가 정확히 2026-06-30인 경우만 추가
            if dt_kst.strftime("%Y-%m-%d") == "2026-06-30":
                # UIManager에서 쓰기 편하게 KST 시간 정보를 주입
                game['display_date'] = dt_kst.strftime("%m월 %d일")
                game['display_time'] = dt_kst.strftime("%H:%M")
                filtered_data.append(game)
        except:
            continue
            
    return filtered_data

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ 2026년 6월 30일 한국 시간 MLB 경기")
    
    if st.button("🔄 데이터 새로고침"):
        st.rerun()
        
    games = get_filtered_mlb_data()
    
    if games:
        UIManager.render_game_navbar(games)
    else:
        st.info("한국 시간 6월 30일 진행되는 경기가 리스트에 없습니다. (데이터 업데이트 지연 가능성)")

if __name__ == "__main__":
    main()
