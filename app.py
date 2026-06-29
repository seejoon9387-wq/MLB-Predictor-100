import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

st.set_page_config(page_title="MLB AI Analyst", layout="wide")

@st.cache_data(ttl=600)
def get_mlb_schedule():
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={today}&endDate={today}"
    response = requests.get(url)
    data = response.json()
    
    games = []
    kst = pytz.timezone('Asia/Seoul')
    
    if 'dates' in data:
        for date_entry in data['dates']:
            for game in date_entry.get('games', []):
                # 경기 시간 변환
                time_utc = datetime.fromisoformat(game['gameDate'].replace('Z', '+00:00'))
                time_kst = time_utc.astimezone(kst)
                
                games.append({
                    'Time': time_kst.strftime('%H:%M'),
                    'Away': game['teams']['away']['team']['name'],
                    'Away_Wins': game['teams']['away']['leagueRecord']['wins'],
                    'Home': game['teams']['home']['team']['name'],
                    'Home_Wins': game['teams']['home']['leagueRecord']['wins']
                })
    return pd.DataFrame(games)

def main():
    st.title("⚾ MLB 실시간 매치업 분석 대시보드")
    df = get_mlb_schedule()
    
    if df.empty:
        st.info("오늘 예정된 경기가 없습니다.")
        return

    # 경기 목록 출력
    st.subheader("📅 오늘의 경기 일정 (KST)")
    event = st.dataframe(df, use_container_width=True, hide_index=True, selection_mode="single-row", on_select="rerun")
    
    if event.selection.rows:
        idx = event.selection.rows[0]
        selected = df.iloc[idx]
        
        st.divider()
        st.subheader(f"🔍 {selected['Away']} vs {selected['Home']} 분석")
        
        if st.button("🚀 AI 분석 리포트 생성"):
            # 투수 정보가 없을 경우 대비한 분석 시뮬레이션
            with st.spinner('AI 분석 엔진 가동 중...'):
                st.success("데이터 기반 분석 완료!")
                
                # 데이터 기반 승률 비교
                total_wins = selected['Away_Wins'] + selected['Home_Wins']
                away_prob = round((selected['Away_Wins'] / total_wins) * 100)
                home_prob = 100 - away_prob
                
                col1, col2 = st.columns(2)
                col1.metric(f"{selected['Away']} 승리 확률", f"{away_prob}%")
                col2.metric(f"{selected['Home']} 승리 확률", f"{home_prob}%")
                st.progress(home_prob / 100)
                
                st.write("---")
                st.markdown(f"""
                **[AI 매치업 요약]**
                * **시즌 기록 기반:** {selected['Away']}은 시즌 {selected['Away_Wins']}승, {selected['Home']}은 {selected['Home_Wins']}승을 기록 중입니다.
                * **전략 분석:** 승률 데이터를 기반으로 분석한 결과, 양 팀의 최근 승패 밸런스는 {'박빙' if abs(away_prob-home_prob) < 10 else '어느 정도 차이가 있는'} 상태입니다.
                * **참고:** 선발 투수 확정 데이터가 추가되는 대로 더 정밀한 투수별 방어율 분석 리포트를 제공할 예정입니다.
                """)

if __name__ == "__main__":
    main()
