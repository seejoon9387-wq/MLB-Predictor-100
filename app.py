import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    # 오늘부터 7일간의 일정 조회
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={datetime.now().strftime('%Y-%m-%d')}"
    response = requests.get(url)
    data = response.json()
    
    games = []
    kst = pytz.timezone('Asia/Seoul')
    
    for date_entry in data.get('dates', []):
        for game in date_entry.get('games', []):
            # UTC 시간을 KST로 변환
            game_time_utc = datetime.fromisoformat(game['gameDate'].replace('Z', '+00:00'))
            game_time_kst = game_time_utc.astimezone(kst)
            
            games.append({
                'Date': game_time_kst.strftime('%m-%d'),
                'Time': game_time_kst.strftime('%H:%M'),
                'Away': game['teams']['away']['team']['name'],
                'Home': game['teams']['home']['team']['name'],
                'Full_Data': game # 분석 엔진에 넘길 상세 데이터
            })
            
    return pd.DataFrame(games)

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
    df = get_live_schedule()
    
    # 경기 선택 테이블 (인덱스 숨김)
    event = st.dataframe(
        df[['Date', 'Time', 'Away', 'Home']], 
        use_container_width=True, 
        hide_index=True,
        selection_mode="single-row",
        on_select="rerun"
    )
    
    # 분석 버튼 로직
    if event.selection.rows:
        idx = event.selection.rows[0]
        selected = df.iloc[idx]
        
        st.divider()
        st.subheader(f"🔍 {selected['Away']} vs {selected['Home']} 분석")
        st.write(f"경기 시간: {selected['Date']} {selected['Time']} (KST)")
        
        if st.button("🚀 엔진 가동 (분석 시작)"):
            with st.spinner('AI 분석 엔진 가동 중...'):
                # 여기서 실제 분석 로직 실행
                st.success("데이터 분석이 완료되었습니다!")
                st.info("분석 결과: [승리 예측 등 상세 리포트가 여기에 표시됩니다]")

if __name__ == "__main__":
    main()
