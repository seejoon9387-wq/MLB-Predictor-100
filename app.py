import streamlit as st
import statsapi

def get_mlb_data():
    try:
        # 데이터가 없을 경우를 대비한 예외 처리
        schedule = statsapi.schedule(date='2026-06-30')
        return schedule if schedule else []
    except:
        return []

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ 2026년 6월 30일 MLB 실시간 경기")
    
    if st.button("🔄 실시간 업데이트"):
        st.cache_data.clear()
        st.rerun()
        
    games = get_mlb_data()
    
    if games:
        from modules.ui_manager import UIManager
        UIManager.render_game_navbar(games)
    else:
        st.info("오늘 예정된 경기가 없거나 데이터를 불러오지 못했습니다.")

if __name__ == "__main__":
    main()
