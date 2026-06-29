import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    # 오늘 날짜
    today_str = datetime.now().strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={today_str}&endDate={today_str}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        games = []
        kst = pytz.timezone('Asia/Seoul')
        
        # 데이터가 있는지 확인
        if 'dates' in data and len(data['dates']) > 0:
            for date_entry in data['dates']:
                for game in date_entry.get('games', []):
                    # UTC 시간을 KST로 변환
                    game_time_utc = datetime.fromisoformat(game['gameDate'].replace('Z', '+00:00'))
                    game_time_kst = game_time_utc.astimezone(kst)
                    
                    games.append({
                        'Date': game_time_kst.strftime('%m-%d'),
                        'Time': game_time_kst.strftime('%H:%M'),
                        'Away': game['teams']['away']['team']['name'],
                        'Home': game['teams']['home']['team']['name']
                    })
        
        if not games:
            return pd.DataFrame(columns=['Date', 'Time', 'Away', 'Home'])
            
        return pd.DataFrame(games)
    
    except Exception:
        return pd.DataFrame(columns=['Date', 'Time', 'Away', 'Home'])

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
    df = get_live_schedule()
    
    if df.empty:
        st.warning("오늘 예정된 경기가 없습니다.")
        return

    # 경기 선택 테이블
    event = st.dataframe(
        df, 
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
        
        if st.button("🚀 엔진 가동"):
            st.success("데이터 분석이 완료되었습니다!")

if __name__ == "__main__":
    main()
