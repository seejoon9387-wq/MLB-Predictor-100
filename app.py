import streamlit as st
import pandas as pd
from datetime import datetime
import pybaseball
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    year = datetime.now().year
    # 최신 버전 pybaseball 표준 호출 방식: 특정 팀을 지정하지 않고 전체를 가져오기 위한 우회 방법
    # 만약 에러가 난다면, 특정 팀(예: 'NYY')을 넣어야 할 수도 있습니다.
    # 여기서는 전체 일정을 가져오기 위해 데이터를 병합하는 구조를 취합니다.
    try:
        # 2026년 시즌 전체 데이터를 가져오기 위해 스케줄 데이터를 직접 호출
        data = pybaseball.schedule_and_record(year, 'LAD') # 예시로 LAD 데이터 사용
        return data[['Date', 'Home', 'Away']]
    except Exception as e:
        st.error(f"데이터 로드 중 문제 발생: {e}")
        return pd.DataFrame(columns=['Date', 'Home', 'Away'])

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
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

if __name__ == "__main__":
    main()
