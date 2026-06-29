import streamlit as st
import statsapi
from datetime import datetime
import pytz
from modules.ui_manager import UIManager

def get_kst_time(utc_iso_string):
    try:
        # UTC 시간 파싱
        dt = datetime.strptime(utc_iso_string, "%Y-%m-%dT%H:%M:%SZ")
        dt = dt.replace(tzinfo=pytz.utc)
        # 한국 시간(KST)으로 변환
        return dt.astimezone(pytz.timezone('Asia/Seoul')).strftime("%H:%M")
    except:
        return "--:--"

def main():
    st.title("⚾ MLB 실시간 경기")
    
    # 1. 데이터 가져오기
    raw_games = statsapi.schedule(date=datetime.now().strftime('%Y-%m-%d'))
    
    # 2. 데이터 가공
    games = []
    for g in raw_games:
        games.append({
            "display_date": g['game_date'],
            "display_time": get_kst_time(g['game_datetime']),
            "away_name": g['away_name'],
            "away_score": g.get('away_score', 0),
            "home_name": g['home_name'],
            "home_score": g.get('home_score', 0)
        })
    
    # 3. UI 렌더링
    UIManager.render_game_navbar(games)

if __name__ == "__main__":
    main()
