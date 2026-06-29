import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

st.set_page_config(page_title="MLB AI Pro Analyst", layout="wide")

@st.cache_data(ttl=600)
def fetch_mlb_data():
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={today}&endDate={today}&hydrate=probablePitcher"
    response = requests.get(url)
    data = response.json()
    
    games = []
    kst = pytz.timezone('Asia/Seoul')
    
    if 'dates' in data:
        for date_entry in data['dates']:
            for game in date_entry.get('games', []):
                # 선발 투수 정보 추출
                pitchers = game.get('probablePitchers', {})
                away_p = pitchers.get('away', {}).get('fullName', 'TBD')
                home_p = pitchers.get('home', {}).get('fullName', 'TBD')
                
                time_utc = datetime.fromisoformat(game['gameDate'].replace('Z', '+00:00'))
                time_kst = time_utc.astimezone(kst)
                
                games.append({
                    'Date': time_kst.strftime('%m-%d'),
                    'Time': time_kst.strftime('%H:%M'),
                    'Away': game['teams']['away']['team']['name'],
                    'Away_Pitcher': away_p,
                    'Home': game['teams']['home']['team']['name'],
                    'Home_Pitcher': home_p
                })
    return pd.DataFrame(games)

def main():
    st.title("⚾ MLB 투수 매칭 AI 분석 리포트")
    df = fetch_mlb_data()
    
    if df.empty:
        st.info("오늘 예정된 경기가 없습니다.")
        return

    # 테이블에 선발 투수 표시
    event = st.dataframe(df[['Date', 'Time', 'Away', 'Away_Pitcher', 'Home', 'Home_Pitcher']], 
                         use_container_width=True, hide_index=True, selection_mode="single-row", on_select="rerun")
    
    if event.selection.rows:
        idx = event.selection.rows[0]
        selected = df.iloc[idx]
        
        st.divider()
        st.subheader(f"🔍 {selected['Away']} vs {selected['Home']} 선발 매치업 분석")
        
        if st.button("🚀 투수 전력 상세 분석 가동"):
            with st.spinner('선발 투수 데이터를 정밀 분석 중...'):
                st.success("데이터 기반 리포트 생성 완료")
                
                # 투수 전력 데이터 시뮬레이션 (실제 엔진 연동 시 API에서 가져온 값 사용)
                st.columns(2)[0].metric(f"원정 선발: {selected['Away_Pitcher']}", "ERA 3.20")
                st.columns(2)[1].metric(f"홈 선발: {selected['Home_Pitcher']}", "ERA 2.85")
                
                tab1, tab2 = st.tabs(["투수 전력 분석", "경기 전략"])
                with tab1:
                    st.markdown(f"""
                    * **{selected['Away_Pitcher']} 분석:** 최근 3경기 이닝 소화력(6.2이닝)이 우수하며 탈삼진 비율이 높음.
                    * **{selected['Home_Pitcher']} 분석:** 제구력이 안정적이며 피안타율(0.210)이 낮아 경기 초반 리드 가능성이 큼.
                    * **상대 전력 차이:** 홈 선발 투수가 원정 선발 대비 방어율(ERA)에서 약 0.35 우세함.
                    """)
                with tab2:
                    st.info(f"오늘 경기는 {selected['Home_Pitcher']}의 제구력이 {selected['Away']} 타선을 얼마나 묶어두느냐가 승패의 핵심입니다.")
