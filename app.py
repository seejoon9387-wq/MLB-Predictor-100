import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

st.title("⚾ MLB 예측 분석 엔진 v2.2 (통합 분석 모드)")

# 1. 모델 로드
@st.cache_resource
def load_model():
    if os.path.exists('mlb_model.pkl'):
        return joblib.load('mlb_model.pkl')
    return None

model = load_model()

# 2. 사이드바 입력 (중복 ID 방지용 key 추가)
st.sidebar.header("경기 및 타구 데이터 입력")
home_team = st.sidebar.text_input("홈 팀 이름", value="Home Team", key="home_input")
away_team = st.sidebar.text_input("원정 팀 이름", value="Away Team", key="away_input")

st.sidebar.divider()

launch_angle = st.sidebar.number_input("Launch Angle", value=15.0, step=0.1, key="la")
bat_speed = st.sidebar.number_input("Bat Speed", value=70.0, step=0.1, key="bs")
release_speed = st.sidebar.number_input("Release Speed", value=90.0, step=0.1, key="rs")
hyper_speed = st.sidebar.number_input("Hyper Speed", value=100.0, step=0.1, key="hs")
release_extension = st.sidebar.number_input("Release Extension", value=6.0, step=0.1, key="re")

# 3. 분석 실행
if st.button("안타 확률 예측 및 분석"):
    if model is None:
        st.error("모델 파일(mlb_model.pkl)을 찾을 수 없습니다.")
    else:
        st.subheader(f"경기 분석: {home_team} vs {away_team}")
        input_data = pd.DataFrame([[launch_angle, bat_speed, release_speed, hyper_speed, release_extension]], 
                                  columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
        
        proba = model.predict_proba(input_data)[0][1]
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = proba * 100,
            title = {'text': "예측 안타 확률 (%)"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
        ))
        st.plotly_chart(fig, use_container_width=True)
