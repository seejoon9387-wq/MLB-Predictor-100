import streamlit as st
import pandas as pd
from datetime import datetime
import pybaseball
import re
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    year = datetime.now().year
    df = pybaseball.schedule_and_record(year, 'LAD')
    df = df.reset_index()
    
    # 1. 날짜 데이터 정제
    def clean_date(date_str):
        # 요일과 콤마 제거 ("Thursday, " -> "")
        date_str = re.sub(r'^[A-Za-z]+, ', '', str(date_str))
        # 연도가 없는 경우(예: "Mar 26") 올해 연도 붙이기
        if ',' not in date_str:
            date_str = f"{date_str}, {year}"
        return date_str

    df['Date'] = df['Date'].apply(clean_date)
    
    # 2. 날짜 형식 변환
    df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')
    
    # 3. Home/Away 구분 로직
    df['Away'] = df.apply(lambda x: x['Tm'] if x['Home_Away'] == '@' else x['Opp'], axis=1)
    df['Home'] = df.apply(lambda x: x['Opp'] if x['Home_Away'] == '@' else x['Tm'], axis=1)
    
    # 4. 오늘 이후 경기만 필터링 및 정렬
    today = pd.Timestamp(datetime.now().date())
    df = df[df['Date'] >= today].sort_values(by='Date').reset_index(drop=True)
    
    # 5. 보기 좋은 형식으로 변환
    df['Display_Date'] = df['Date'].dt.strftime('%m-%d (%a)')
    
    return df[['Date', 'Display_Date', 'Away', 'Home']]

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
    try:
        df = get_live_schedule()
        
        if df.empty:
            st.warning("현재 예정된 경기가 없습니다.")
            return

        st.subheader("📅 오늘의 경기 및 향후 일정")
        
        # 경기 일정 선택 표
        event = st.dataframe(
            df[['Display_Date', 'Away', 'Home']], 
            use_container_width=True,
            hide_index=True,
            selection_mode="single-row",
            on_select="rerun"
        )
        
        if event.selection.rows:
            idx = event.selection.rows[0]
            selected_game = df.iloc[idx]
            
            st.divider()
            st.write(f"### 🔍 분석 대상: {selected_game['Away']} vs {selected_game['Home']} ({selected_game['Display_Date']})")
            
            if st.button("🚀 엔진 가동"):
                st.info("데이터 분석 엔진을 가동합니다...")
                
    except Exception as e:
        st.error(f"데이터 처리 오류: {e}")
        st.write("문제가 지속되면 데이터의 원본 형식을 확인해야 합니다.")

if __name__ == "__main__":
    main()
