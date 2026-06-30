import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

# 1. 모델 로드
@st.cache_resource
def load_model():
    if os.path.exists('mlb_model.pkl'):
        return joblib.load('mlb_model.pkl')
    return None

model = load_model()

# 2. 경기 일정 데이터
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"}, {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"}, {"home": "ATL", "away": "PHI", "time": "20:00"},
    {"home": "SEA", "away": "HOU", "time": "21:00"}, {"home": "TEX", "away": "OAK", "time": "21:30"}
]

# 3. 경기 일정 표시 (기본 UI 사용)
st.title("⚾ MLB 예측 분석 엔진 v2.2")
st.subheader("🗓️ 실시간 경기 일정")

if 'page' not in st.session_state: st.session_state.page = 0

# 화살표와 3개의 경기를 기본 컴포넌트로 표시
c1, c2, c3, c4, c5 = st.columns([1, 2, 2, 2, 1])

with c1:
    if st.button("◀️ 이전"): st.session_state.page = max(0, st.session_state.page - 1)

# 현재 페이지의 경기 보여주기 (3개씩)
current = matches[st.session_state.page*3 : (st.session_state.page+1)*3]
for i, col in enumerate([c2, c3, c4]):
    if i < len(current):
        with col:
            st.metric(label=f"{current[i]['home']} vs {current[i]['away']}", value=current[i]['time'])

with c5:
    if st.button("다음 ▶️"): st.session_state.page += 1

# 4. 분석 실행
st.divider()
st.sidebar.header("📊 데이터 입력")
home = st.sidebar.text_input("홈 팀", value="Home")
away = st.sidebar.text_input("원정 팀", value="Away")
la = st.sidebar.number_input("Launch Angle", value=15.0)
bs = st.sidebar.number_input("Bat Speed", value=70.0)
rs = st.sidebar.number_input("Release Speed", value=90.0)
hs = st.sidebar.number_input("Hyper Speed", value=100.0)
re = st.sidebar.number_input("Release Extension", value=6.0)

if st.button("🚀 결과 분석 실행"):
    if model:
        input_data = pd.DataFrame([[la, bs, rs, hs, re]], 
                                  columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
        proba = model.predict_proba(input_data)[0][1]
        
        st.subheader(f"결과: {home} vs {away}")
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=proba * 100, title={'text': "안타 확률 (%)"},
            gauge={'axis': {'range': [0, 100]}}
        ))
        st.plotly_chart(fig)
    else:
        st.error("모델 파일(mlb_model.pkl)을 찾을 수 없습니다.")
