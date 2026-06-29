import streamlit as st
import statsapi
from modules.ui_manager import UIManager

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ 2026년 6월 30일 MLB 실시간 경기")
    
    # 캐시를 즉시 비우고 버튼을 통해 새로고침
    if st.button("🔄 데이터 업데이트"):
        st.cache_data.clear()
        st.rerun()
        
    try:
        games = statsapi.schedule(date='2026-06-30')
        if games:
            UIManager.render_game_navbar(games)
        else:
            st.write("오늘 예정된 경기가 없습니다.")
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
