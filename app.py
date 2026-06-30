import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import os

# 페이지 설정
st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

# 1. 모델 로드
@st.cache_resource
def load_model():
    if os.path.exists('mlb_model.pkl'):
        return joblib.load('mlb_model.pkl')
    return None

model = load_model()

# 2. 사이드바: 입력 컨트롤러
st.sidebar.header("📊 입력 컨트롤러")
home_team = st.sidebar.text_input("홈 팀", value="Home Team", key="home_input")
away_team = st.sidebar.text_input("원정 팀", value="Away Team", key="away_input")

st.sidebar.divider()
launch_angle = st.sidebar.number_input("Launch Angle", value=15.0, step=0.1, key="la")
bat_speed = st.sidebar.number_input("Bat Speed", value=70.0, step=0.1, key="bs")
release_speed = st.sidebar.number_input("Release Speed", value=90.0, step=0.1, key="rs")
hyper_speed = st.sidebar.number_input("Hyper Speed", value=100.0, step=0.1, key="hs")
release_extension = st.sidebar.number_input("Release Extension", value=6.0, step=0.1, key="re")

# 3. 메인 화면: 경기 일정 캐러셀
st.title("⚾ MLB 예측 분석 엔진 v2.2")
st.subheader("🗓️ 실시간 경기 일정")

matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"},
    {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"},
    {"home": "ATL", "away": "PHI", "time": "20:00"},
    {"home": "SEA", "away": "HOU", "time": "21:00"}
]

if 'page' not in st.session_state:
    st.session_state.page = 0

col_left, col_mid, col_right = st.columns([1, 8, 1])

with col_left:
    if st.button("◀️"):
        st.session_state.page = max(0, st.session_state.page - 1)

with col_mid:
    display_matches = matches[st.session_state.page : st.session_state.page + 3]
    cols = st.columns(3)
    for i, match in enumerate(display_matches):
        with cols[i]:
            st.metric(label=f"{match['home']} vs {match['away']}", value=match['time'])

with col_right:
    if st.button("▶️"):
        st.session_state.page = min(len(matches) - 3, st.session_state.page + 1)

# 4. 분석 실행 섹션
st.divider()
st.info("좌측 패널에서 데이터를 입력한 후 아래 버튼을 클릭하여 분석을 시작하세요.")

if st.button("🚀 결과 분석 실행", type="primary"):
    with st.spinner('엔진 가동 중... 확률 계산 중입니다...'):
        if model is None:
            st.error("오류: 모델 파일(mlb_model.pkl)을 찾을 수 없습니다.")
        else:
            input_data = pd.DataFrame([[launch_angle, bat_speed, release_speed, hyper_speed, release_extension]], 
                                      columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
            
            proba = model.predict_proba(input_data)[0][1]
            
            st.subheader(f"결과: {home_team} vs {away_team}")
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = proba * 100,
                title = {'text': "안타 확률 (%)"},
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#1f77b4"}}
            ))
            st.plotly_chart(fig, use_container_width=True)
            st.success("분석이 완료되었습니다.")
