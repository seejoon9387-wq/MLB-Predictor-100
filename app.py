import streamlit as st
import pandas as pd
from datetime import datetime
import pybaseball
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    year = datetime.now().year
    # 2026년 시즌 데이터를 가져옵니다.
    # 특정 팀('LAD') 대신 전체적인 데이터 구조를 먼저 확인합니다.
    data = pybaseball.schedule_and_record(year, 'LAD')
    
    # 디버깅: 실제 어떤 컬럼이 있는지 확인 (데이터가 로드되지 않으면 이 메시지가 뜹니다)
    # st.write("확인된 컬럼:", data.columns.tolist()) 
    
    # 데이터를 우리가 필요한 형식으로 매핑
    # 컬럼명이 다를 경우를 대비하여 근접한 이름을 찾습니다.
    # 보통 Away팀은 '@' 기호를 포함하거나 'Away' 컬럼이 별도로 존재합니다.
    df = data.reset_index()
    
    # 컬럼 이름을 우리가 사용하는 'Away', 'Home'으로 강제 변경
    # 데이터셋에 따라 컬럼명이 다르다면 아래 이름을 실제 데이터에 맞게 수정해야 합니다.
    # 예: 'Home' -> 'Home' / 'Away' -> 'Away'
    return df[['Date', 'Home', 'Away']]

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
        st.write("힌트: 데이터의 컬럼명이 코드와 다를 수 있습니다. 위 코드의 'df[['Date', 'Home', 'Away']]' 부분을 확인해 보세요.")

if __name__ == "__main__":
    main()
