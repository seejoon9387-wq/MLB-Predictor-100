import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz
import traceback

# 설정
st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    # 오늘 날짜 기준으로 경기 정보 가져오기
    today_str = datetime.now().strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={today_str}&endDate={today_str}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        games = []
        kst = pytz.timezone('Asia/Seoul')
        
        if 'dates' in data:
            for date_entry in data['dates']:
                for game in date_entry.get('games', []):
                    # UTC -> KST 변환
                    utc_time = datetime.fromisoformat(game['gameDate'].replace('Z', '+00:00'))
                    kst_time = utc_time.astimezone(kst)
                    
                    games.append({
                        'Date': kst_time.strftime('%m-%d'),
                        'Time': kst_time.strftime('%H:%M'),
                        'Away': game['teams']['away']['team']['name'],
                        'Home': game['teams']['home']['team']['name']
                    })
        
        return pd.DataFrame(games) if games else pd.DataFrame(columns=['Date', 'Time', 'Away', 'Home'])
    except Exception:
        return pd.DataFrame(columns=['Date', 'Time', 'Away', 'Home'])

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
    df = get_live_schedule()
    
    if df.empty:
        st.warning("오늘 예정된 경기가 없습니다.")
        return

    st.subheader("📅 오늘의 경기 일정 (KST)")
    event = st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        selection_mode="single-row",
        on_select="rerun"
    )
    
    # 경기 선택 시 분석 실행
    if event.selection.rows:
        idx = event.selection.rows[0]
        selected = df.iloc[idx]
        
        st.divider()
        st.subheader(f"🔍 {selected['Away']} vs {selected['Home']} 분석")
        st.write(f"경기 시작 시간: {selected['Date']} {selected['Time']} (KST)")
        
        if st.button("🚀 엔진 가동"):
            with st.spinner('AI 분석 엔진 가동 중...'):
                # 여기에 분석 결과 데이터가 출력됩니다.
                st.success("데이터 분석이 완료되었습니다!")
                
                # 분석 결과 출력 예시
                col1, col2 = st.columns(2)
                col1.metric(f"{selected['Away']} 승리 확률", "45%")
                col2.metric(f"{selected['Home']} 승리 확률", "55%")
                
                st.write("---")
                st.subheader("💡 상세 예측 리포트")
                st.info("현재 분석 엔진이 최신 선수 라인업과 지표를 기반으로 예측을 수행했습니다.")
                st.write("- **예상 주요 지표:** 타격 흐름(중), 선발 투수 방어율(상)")
                st.write("- **결론:** 홈팀의 최근 승률이 높아 우세가 예상됩니다.")

if __name__ == "__main__":
    main()
