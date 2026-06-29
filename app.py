import streamlit as st
import pandas as pd
from datetime import datetime
from pybaseball import schedule_and_record
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

# 실시간 데이터 로드 함수
@st.cache_data(ttl=3600) # 1시간 동안 데이터 캐싱
def get_live_schedule():
    year = datetime.now().year
    # 이번 시즌 전체 일정을 가져와서 현재 날짜 이후 경기만 필터링할 수 있음
    df = schedule_and_record(year, 'all')
    # 필요한 데이터 형태로 가공
    df = df.reset_index()
    return df

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
    with st.spinner('MLB 공식 데이터를 불러오는 중...'):
        df = get_live_schedule()
    
    st.subheader("📅 오늘의 경기 일정")
    
    # 경기 일정 표 출력 (사용자가 선택 가능)
    event = st.dataframe(
        df[['Date', 'Home', 'Away']], 
        use_container_width=True,
        selection_mode="single-row",
        on_select="rerun"
    )
    
    # 선택된 경기 분석
    if event.selection.rows:
        idx = event.selection.rows[0]
        selected_game = df.iloc[idx]
        
        st.divider()
        st.write(f"### 분석 대상: {selected_game['Away']} vs {selected_game['Home']} ({selected_game['Date']})")
        
        if st.button("분석 엔진 가동"):
            try:
                # trainer 객체 호출 (실제 game_pk를 매칭해야 함)
                trainer = MLBUnifiedTrainer()
                # briefing = trainer.get_briefing(selected_game['game_pk'])
                st.info("엔진이 분석을 시작합니다... (이곳에 실제 분석 로직이 연결됩니다)")
            except Exception as e:
                st.error(f"분석 오류: {e}")

if __name__ == "__main__":
    main()
