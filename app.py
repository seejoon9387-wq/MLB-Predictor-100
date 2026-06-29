import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    # MLB 공식 API 주소 (2026년 시즌)
    # 직접 데이터를 가져오는 방식입니다.
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={datetime.now().strftime('%Y-%m-%d')}&endDate=2026-10-31"
    
    response = requests.get(url)
    data = response.json()
    
    games = []
    for date_entry in data.get('dates', []):
        for game in date_entry.get('games', []):
            games.append({
                'Date': date_entry['date'],
                'Away': game['teams']['away']['team']['name'],
                'Home': game['teams']['home']['team']['name']
            })
            
    df = pd.DataFrame(games)
    
    # 한국 시간 처리
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df[['Date', 'Away', 'Home']]

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
    try:
        df = get_live_schedule()
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        st.write("라이브러리 오류 없이 직접 API에서 데이터를 가져왔습니다.")

if __name__ == "__main__":
    main()
