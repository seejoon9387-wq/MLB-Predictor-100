import streamlit as st
import statsapi

def get_mlb_data():
    try:
        schedule = statsapi.schedule(date='2026-06-30')
        return schedule
    except:
        return []

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ 2026년 6월 30일 MLB 실시간 경기")
    
    games = get_mlb_data()
    
    # [데이터 확인용 디버깅] - 이 내용이 화면에 뜨면 복사해서 알려주세요!
    if games:
        with st.expander("데이터 상세 보기 (개발자용)"):
            st.write("Raw Data Sample:", games[0]) 
        
        from modules.ui_manager import UIManager
        UIManager.render_game_navbar(games)
    else:
        st.info("데이터가 없습니다.")

if __name__ == "__main__":
    main()
