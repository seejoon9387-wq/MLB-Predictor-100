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
    
    # 1. 날짜 데이터 클리닝: 요일 부분(예: "Thursday, ")을 제거
    # 정규식: 글자, 콤마, 공백이 있는 앞부분을 삭제
    df['Date'] = df['Date'].apply(lambda x: re.sub(r'^[A-Za-z]+, ', '', str(x)))
    
    # 2. 날짜 형식 변환 (이제는 깔끔하게 Mar 26, 2026 형태만 남음)
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
        st.write("데이터의 날짜 형식 문제일 가능성이 높습니다. 로그를 확인해 주세요.")

if __name__ == "__main__":
    main()
