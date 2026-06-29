import streamlit as st
import pandas as pd
from datetime import datetime
import pybaseball
import pytz
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    # 올해 연도 설정
    year = datetime.now().year
    df = pybaseball.schedule_and_record(year, 'LAD')
    df = df.reset_index()
    
    # 1. 날짜 데이터 정제 및 한국 시간 적용
    # format='mixed'는 요일이 있든 없든 연도가 있든 없든 알아서 날짜로 변환합니다.
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    
    # 한국 표준시(KST) 설정 (기본 날짜에 시간 정보를 09:00:00으로 설정)
    kst = pytz.timezone('Asia/Seoul')
    df['Date'] = df['Date'].dt.tz_localize(None).dt.tz_localize('UTC').dt.tz_convert(kst)
    
    # 2. Home/Away 구분 로직
    df['Away'] = df.apply(lambda x: x['Tm'] if x['Home_Away'] == '@' else x['Opp'], axis=1)
    df['Home'] = df.apply(lambda x: x['Opp'] if x['Home_Away'] == '@' else x['Tm'], axis=1)
    
    # 3. 오늘(KST 기준) 이후 경기만 필터링 및 정렬
    today = datetime.now(kst).replace(tzinfo=None)
    df = df[df['Date'].dt.tz_localize(None) >= today].sort_values(by='Date').reset_index(drop=True)
    
    # 4. 보기 좋은 형식으로 변환 (KST 기준)
    df['Display_Date'] = df['Date'].dt.strftime('%m-%d (%a)')
    
    return df[['Date', 'Display_Date', 'Away', 'Home']]

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
    try:
        df = get_live_schedule()
        
        if df.empty:
            st.warning("현재 예정된 경기가 없습니다.")
            return

        st.subheader("📅 오늘의 경기 및 향후 일정 (KST 기준)")
        
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
        st.write("데이터 형식이 여전히 문제가 있다면 다시 알려주세요.")

if __name__ == "__main__":
    main()
