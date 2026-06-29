import streamlit as st
import pandas as pd
from datetime import datetime
import pybaseball
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    # 올해 연도 설정
    year = datetime.now().year
    
    # LAD 데이터 로드
    df = pybaseball.schedule_and_record(year, 'LAD')
    df = df.reset_index()
    
    # 1. 날짜 데이터 형식 변환 (예: "Jun 29" -> 2026-06-29)
    df['Date'] = pd.to_datetime(df['Date'] + f", {year}", format='%b %d, %Y')
    
    # 2. Home/Away 구분 로직
    df['Away'] = df.apply(lambda x: x['Tm'] if x['Home_Away'] == '@' else x['Opp'], axis=1)
    df['Home'] = df.apply(lambda x: x['Opp'] if x['Home_Away'] == '@' else x['Tm'], axis=1)
    
    # 3. 오늘 이후 경기만 필터링 및 날짜순 정렬
    today = pd.Timestamp(datetime.now().date())
    df = df[df['Date'] >= today].sort_values(by='Date').reset_index(drop=True)
    
    # 4. 보기 좋은 형식으로 변환
    df['Display_Date'] = df['Date'].dt.strftime('%m-%d (%a)')
    
    return df[['Date', 'Display_Date', 'Away', 'Home']]

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
    try:
        df = get_live_schedule()
        st.subheader("📅 오늘의 경기 및 향후 일정")
        
        # 표 출력 (날짜, 원정팀, 홈팀만 표시)
        event = st.dataframe(
            df[['Display_Date', 'Away', 'Home']], 
            use_container_width=True,
            hide_index=True,
            selection_mode="single-row",
            on_select="rerun"
        )
        
        # 선택된 경기 분석
        if event.selection.rows:
            idx = event.selection.rows[0]
            selected_game = df.iloc[idx]
            
            st.divider()
            st.write(f"### 🔍 분석 대상: {selected_game['Away']} vs {selected_game['Home']} ({selected_game['Display_Date']})")
            
            if st.button("🚀 엔진 가동"):
                st.info("데이터 분석 엔진을 가동합니다...")
                # trainer = MLBUnifiedTrainer()
                # briefing = trainer.get_briefing(selected_game)
                
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
