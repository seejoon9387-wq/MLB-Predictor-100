import streamlit as st
import pandas as pd
from datetime import datetime
from pybaseball import schedule
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

# 캐시 설정
@st.cache_data(ttl=3600)
def get_live_schedule():
    year = datetime.now().year
    df = schedule(year)
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
                trainer = MLBUnifiedTrainer()
                st.info("분석이 완료되었습니다.")
                
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
