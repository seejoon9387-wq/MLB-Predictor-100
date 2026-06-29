import streamlit as st
import pandas as pd
from datetime import datetime
import pybaseball
from modules.main_trainer import MLBUnifiedTrainer

# 앱 설정
st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    # 올해 연도 설정
    year = datetime.now().year
    
    # LAD 팀 데이터 로드
    df = pybaseball.schedule_and_record(year, 'LAD')
    df = df.reset_index()
    
    # 1. 날짜 데이터 형식 변환 (format='mixed'로 다양한 형식 자동 감지)
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    
    # 2. Home/Away 구분 로직
    # Home_Away 컬럼에 '@'가 있으면 원정(Away), 없으면 홈(Home)
    df['Away'] = df.apply(lambda x: x['Tm'] if x['Home_Away'] == '@' else x['Opp'], axis=1)
    df['Home'] = df.apply(lambda x: x['Opp'] if x['Home_Away'] == '@' else x['Tm'], axis=1)
    
    # 3. 오늘 이후 경기만 필터링 및 날짜순 정렬
    today = pd.Timestamp(datetime.now().date())
    df = df[df['Date'] >= today].sort_values(by='Date').reset_index(drop=True)
    
    # 4. 화면 표시용 날짜 포맷 (월-일 요일)
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
        
        # 경기 선택 시 분석 엔진 로직
        if event.selection.rows:
            idx = event.selection.rows[0]
            selected_game = df.iloc[idx]
            
            st.divider()
            st.write(f"### 🔍 분석 대상: {selected_game['Away']} vs {selected_game['Home']} ({selected_game['Display_Date']})")
            
            if st.button("🚀 엔진 가동 (분석 시작)"):
                with st.spinner('분석 중...'):
                    # 실제 trainer 객체 사용
                    trainer = MLBUnifiedTrainer()
                    st.success("데이터 분석이 완료되었습니다.")
                    st.info("여기에 분석 결과(승률 예측, 주요 지표 등)가 출력됩니다.")
                
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        st.write("문제가 지속되면 로그를 확인해주세요.")

if __name__ == "__main__":
    main()import streamlit as st
import pandas as pd
from datetime import datetime
import pybaseball
from modules.main_trainer import MLBUnifiedTrainer

# 앱 설정
st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    # 올해 연도 설정
    year = datetime.now().year
    
    # LAD 팀 데이터 로드
    df = pybaseball.schedule_and_record(year, 'LAD')
    df = df.reset_index()
    
    # 1. 날짜 데이터 형식 변환 (format='mixed'로 다양한 형식 자동 감지)
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    
    # 2. Home/Away 구분 로직
    # Home_Away 컬럼에 '@'가 있으면 원정(Away), 없으면 홈(Home)
    df['Away'] = df.apply(lambda x: x['Tm'] if x['Home_Away'] == '@' else x['Opp'], axis=1)
    df['Home'] = df.apply(lambda x: x['Opp'] if x['Home_Away'] == '@' else x['Tm'], axis=1)
    
    # 3. 오늘 이후 경기만 필터링 및 날짜순 정렬
    today = pd.Timestamp(datetime.now().date())
    df = df[df['Date'] >= today].sort_values(by='Date').reset_index(drop=True)
    
    # 4. 화면 표시용 날짜 포맷 (월-일 요일)
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
        
        # 경기 선택 시 분석 엔진 로직
        if event.selection.rows:
            idx = event.selection.rows[0]
            selected_game = df.iloc[idx]
            
            st.divider()
            st.write(f"### 🔍 분석 대상: {selected_game['Away']} vs {selected_game['Home']} ({selected_game['Display_Date']})")
            
            if st.button("🚀 엔진 가동 (분석 시작)"):
                with st.spinner('분석 중...'):
                    # 실제 trainer 객체 사용
                    trainer = MLBUnifiedTrainer()
                    st.success("데이터 분석이 완료되었습니다.")
                    st.info("여기에 분석 결과(승률 예측, 주요 지표 등)가 출력됩니다.")
                
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        st.write("문제가 지속되면 로그를 확인해주세요.")

if __name__ == "__main__":
    main()
