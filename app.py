import streamlit as st
import statsapi

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 테스트 페이지")
    
    st.write("데이터를 가져오는 중...")
    
    try:
        # 오늘 날짜 경기 테스트
        games = statsapi.schedule(date='2026-06-30')
        st.write(f"가져온 경기 수: {len(games)}")
        
        if games:
            for game in games:
                st.write(f"경기 정보: {game.get('summary', '정보 없음')}")
        else:
            st.write("오늘 예정된 경기가 없습니다.")
            
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
