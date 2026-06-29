import streamlit as st
import pandas as pd
from datetime import datetime
from pybaseball import schedule
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

# 실시간 데이터 로드 함수 수정
@st.cache_data(ttl=3600)
def get_live_schedule():
    year = datetime.now().year
    # 'all' 대신 특정 팀을 지정하지 않는 schedule 함수 사용
    df = schedule(year)
    
    # 필요한 컬럼만 추출 및 정리
    # pybaseball의 schedule은 ['Date', 'Away', 'Home', ...] 형식을 가짐
    df = df[['Date', 'Away', 'Home']]
    return df

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
    with st.spinner('MLB 공식 데이터를 불러오는 중...'):
        try:
            df = get_live_schedule()
            
            st.subheader("📅 경기 일정")
            
            # 경기 일정 표 출력
            event = st.dataframe(
                df, 
                use_container_width=True,
                selection_mode="single-row",
                on_select="rerun"
            )
            
            # 선택된 경기 분석 로직
            if event.selection.rows:
                idx = event.selection.rows[0]
                selected_game = df.iloc[idx]
                
                st.divider()
                st.write(f"### 분석 대상: {selected_game['Away']} vs {selected_game['Home']} ({selected_game['Date']})")
                
                if st.button("분석 엔진 가동"):
                    st.info("선택된 경기에 대한 데이터 분석을 시작합니다.")
                    # trainer = MLBUnifiedTrainer()
                    # briefing = trainer.get_briefing(selected_game)
                    
        except Exception as e:
            st.error(f"데이터 로드 중 오류 발생: {e}")
            st.write("힌트: 네트워크 환경이나 pybaseball 라이브러리 연결을 확인하세요.")

if __name__ == "__main__":
    main()
