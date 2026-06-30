import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

# 1. 모델 로드
@st.cache_resource
def load_model():
    return joblib.load('mlb_model.pkl') if os.path.exists('mlb_model.pkl') else None

model = load_model()

st.title("⚾ MLB 예측 분석 엔진 v2.2")
st.subheader("🗓️ 실시간 경기 일정")

# 2. 경기 데이터 (안정적인 리스트)
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"}, {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"}, {"home": "ATL", "away": "PHI", "time": "20:00"},
    {"home": "SEA", "away": "HOU", "time": "21:00"}, {"home": "TEX", "away": "OAK", "time": "21:30"}
]

# 3. 경기 일정 표시 (기본 컴포넌트 사용)
if 'page' not in st.session_state: st.session_state.page = 0

# 화살표 및 경기 목록
c1, c2, c3, c4 = st.columns([1, 8, 8, 1])

with c1:
    if st.button("◀️"): st.session_state.page = max(0, st.session_state.page - 1)

# 경기 카드 표시 (기본 metric 컴포넌트 사용으로 오류 방지)
current_matches = matches[st.session_state.page*3 : (st.session_state.page+1)*3]
for i, match in enumerate([c2, c3, st.columns(3)[0]]): # 3개씩 표시
    if i < len(current_matches):
        with [c2, c3, st.columns(3)[0]][i]:
            st.metric(label=f"{current_matches[i]['home']} vs {current_matches[i]['away']}", 
                      value=current_matches[i]['time'])

with c4:
    if st.button("▶️"): st.session_state.page += 1

# 4. 분석 기능
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
        st.write(f"### {home} vs {away} 안타 확률: {proba*100:.2f}%")
    else:
        st.error("모델 파일을 찾을 수 없습니다.")
