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

# 2. 유동적인 경기 데이터 (리스트 길이에 상관없이 작동)
# 예시: 오늘 경기가 2개일 때도, 15개일 때도 아래 코드 하나로 해결됩니다.
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"},
    {"home": "NYY", "away": "BOS", "time": "19:00"}
    # 여기에 데이터가 100개가 추가되어도 코드는 수정할 필요가 없습니다.
]

st.title("⚾ MLB 예측 분석 엔진")

# 3. 경기 수에 따라 가변적으로 변하는 Expander UI
with st.expander(f"🗓️ 오늘 진행되는 경기 일정 ({len(matches)}경기)", expanded=True):
    for i, match in enumerate(matches):
        # 각 경기를 클릭 가능한 버튼 형태로 배치
        if st.button(f"{match['time']} | {match['home']} vs {match['away']}", key=f"match_{i}"):
            st.session_state.target_home = match['home']
            st.session_state.target_away = match['away']
            st.rerun()

# 4. 분석할 경기 정보 (선택된 데이터 반영)
if 'target_home' not in st.session_state: st.session_state.target_home = matches[0]['home']
if 'target_away' not in st.session_state: st.session_state.target_away = matches[0]['away']

st.subheader(f"✅ 선택된 경기: {st.session_state.target_home} vs {st.session_state.target_away}")

# 5. 분석 로직 (기존과 동일)
st.sidebar.header("📊 데이터 입력")
home = st.sidebar.text_input("홈 팀", value=st.session_state.target_home)
away = st.sidebar.text_input("원정 팀", value=st.session_state.target_away)
la = st.sidebar.number_input("Launch Angle", value=15.0)
bs = st.sidebar.number_input("Bat Speed", value=70.0)
rs = st.sidebar.number_input("Release Speed", value=90.0)
hs = st.sidebar.number_input("Hyper Speed", value=100.0)
re = st.sidebar.number_input("Release Extension", value=6.0)

if st.button("🚀 결과 분석 실행", type="primary"):
    if model:
        input_data = pd.DataFrame([[la, bs, rs, hs, re]], columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
        proba = model.predict_proba(input_data)[0][1]
        
        st.subheader(f"결과: {home} vs {away}")
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=proba * 100, title={'text': "안타 확률 (%)"},
            gauge={'axis': {'range': [0, 100]}}
        ))
        st.plotly_chart(fig)
    else:
        st.error("모델 파일(mlb_model.pkl)을 찾을 수 없습니다.")
