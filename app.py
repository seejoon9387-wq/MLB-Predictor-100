import streamlit as st
import pandas as pd
from datetime import datetime
import pybaseball
import pytz
import traceback

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

# 캐시를 너무 길게 잡지 않고 명확히 설정
@st.cache_data(ttl=600) 
def get_live_schedule():
    year = datetime.now().year
    # LAD 데이터 로드
    df = pybaseball.schedule_and_record(year, 'LAD')
    df = df.reset_index()
    
    # 날짜 처리
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    kst = pytz.timezone('Asia/Seoul')
    df['Date'] = df['Date'].dt.tz_localize(None).dt.tz_localize('UTC').dt.tz_convert(kst)
    
    # 데이터 정리
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
    except Exception:
        st.error("데이터 로드 중 일시적인 오류 발생")
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
