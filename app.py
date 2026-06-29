import streamlit as st
import pandas as pd
from datetime import datetime
import pybaseball
import pytz
import re

# 모듈 임포트 에러 방지 (파일이 없거나 오류가 나도 앱은 띄움)
try:
    from modules.main_trainer import MLBUnifiedTrainer
except ImportError:
    MLBUnifiedTrainer = None

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    # 올해 연도 설정
    year = datetime.now().year
    # 버전을 명시하지 않고 호출 (라이브러리 자체가 알아서 최적의 버전을 선택하게 함)
    df = pybaseball.schedule_and_record(year, 'LAD')
    df = df.reset_index()
    
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    kst = pytz.timezone('Asia/Seoul')
    df['Date'] = df['Date'].dt.tz_localize(None).dt.tz_localize('UTC').dt.tz_convert(kst)
    
    df['Away'] = df.apply(lambda x: x['Tm'] if x['Home_Away'] == '@' else x['Opp'], axis=1)
    df['Home'] = df.apply(lambda x: x['Opp'] if x['Home_Away'] == '@' else x['Tm'], axis=1)
    
    today = datetime.now(kst).replace(tzinfo=None)
    df = df[df['Date'].dt.tz_localize(None) >= today].sort_values(by='Date').reset_index(drop=True)
    df['Display_Date'] = df['Date'].dt.strftime('%m-%d (%a)')
    
    return df[['Date', 'Display_Date', 'Away', 'Home']]

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    try:
        df = get_live_schedule()
        st.dataframe(df[['Display_Date', 'Away', 'Home']], use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"앱 초기화 오류: {e}")

if __name__ == "__main__":
    main()
