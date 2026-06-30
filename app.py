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

# 2. 세션 상태 관리 (클릭 시 팀 이름 저장)
if 'target_home' not in st.session_state: st.session_state.target_home = "Home"
if 'target_away' not in st.session_state: st.session_state.target_away = "Away"

# 3. 경기 데이터
matches = [
    {"home": "LAD", "away": "SF"}, {"home": "NYY", "away": "BOS"},
    {"home": "CHC", "away": "MIL"}, {"home": "ATL", "away": "PHI"}
]

st.title("⚾ MLB 예측 분석 엔진 (클릭 분석 모드)")
st.subheader("🗓️ 경기 선택 (클릭 시 하단에 자동 입력)")

# 4. 경기 카드 배치 (클릭 기능 추가)
cols = st.columns(4)
for i, match in enumerate(matches):
    with cols[i % 4]:
        # 버튼을 누르면 세션 상태가 업데이트됨
        if st.button(f"{match['home']} vs {match['away']}", key=f"btn_{i}"):
            st.session_state.target_home = match['home']
            st.session_state.target_away = match['away']

# 5. 입력 및 분석
st.divider()
st.write(f"### 현재 선택된 경기: **{st.session_state.target_home} vs {st.session_state.target_away}**")

# 자동 입력된 값을 기반으로 동작
home = st.text_input("홈 팀", value=st.session_state.target_home)
away = st.text_input("원정 팀", value=st.session_state.target_away)

la = st.number_input("Launch Angle", value=15.0)
bs = st.number_input("Bat Speed", value=70.0)
rs = st.number_input("Release Speed", value=90.0)
hs = st.number_input("Hyper Speed", value=100.0)
re = st.number_input("Release Extension", value=6.0)

if st.button("🚀 결과 분석 실행"):
    if model:
        input_data = pd.DataFrame([[la, bs, rs, hs, re]], 
                                  columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
        proba = model.predict_proba(input_data)[0][1]
        
        st.subheader(f"분석 결과: {home} vs {away}")
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=proba * 100, title={'text': "안타 확률 (%)"}
        ))
        st.plotly_chart(fig)
    else:
        st.error("모델 파일을 찾을 수 없습니다.")
