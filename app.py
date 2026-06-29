import streamlit as st
import pandas as pd
from datetime import datetime
import pybaseball  # pybaseball 전체를 임포트
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    year = datetime.now().year
    # pybaseball.schedule()을 사용하여 스케줄을 가져옵니다.
    # 만약 여기서도 에러가 난다면 pybaseball.schedule_and_record(year, 'all')로 변경 가능
    df = pybaseball.schedule(year) 
    return df[['Date', 'Away', 'Home']]

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
    try:
        df = get_live_schedule()
        st.subheader("📅 경기 일정")
        
        event = st.dataframe(
            df, 
            use_container_width=True,
            selection_mode="single-row",
            on_select="rerun"
        )
        
        if event.selection.rows:
            idx = event.selection.rows[0]
            selected_game = df.iloc[idx]
            
            st.divider()
            st.write(f"### 🔍 분석 대상: {selected_game['Away']} vs {selected_game['Home']} ({selected_game['Date']})")
            
            if st.button("🚀 엔진 가동"):
                st.info("엔진이 분석을 시작합니다.")
                
    except Exception as e:
        st.error(f"오류 발생: {e}")
        st.write("라이브러리 버전 문제일 수 있습니다. 'pybaseball.schedule' 사용 중 발생한 에러입니다.")

if __name__ == "__main__":
    main()
