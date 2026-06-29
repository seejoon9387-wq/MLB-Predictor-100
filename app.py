import streamlit as st
import statsapi
from datetime import datetime, timedelta
from modules.ui_manager import UIManager

# 1. 데이터 가져오기 로직
def get_filtered_mlb_data():
    raw_data = statsapi.schedule(start_date='2026-06-29', end_date='2026-06-30')
    filtered_data = []
    for game in raw_data:
        try:
            dt_utc = datetime.strptime(game['game_datetime'], "%Y-%m-%dT%H:%M:%SZ")
            dt_kst = dt_utc + timedelta(hours=9)
            if dt_kst.strftime("%Y-%m-%d") == "2026-06-30":
                game['display_date'] = dt_kst.strftime("%m/%d")
                game['display_time'] = dt_kst.strftime("%H:%M")
                filtered_data.append(game)
        except: continue
    return filtered_data

# 2. 메인 실행
def main():
    st.title("⚾ MLB 실시간 경기")
    
    if 'selected_game_id' in st.session_state:
        if st.button("⬅ 목록으로 돌아가기"):
            del st.session_state.selected_game_id
            st.rerun()
        st.write(f"상세 정보 조회 중: ID {st.session_state.selected_game_id}")
        # 여기에 상세 조회 함수 연결
    else:
        games = get_filtered_mlb_data()
        if games:
            UIManager.render_game_navbar(games)
        else:
            st.write("경기가 없습니다.")

if __name__ == "__main__":
    main()
