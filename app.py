import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import os

st.title("MLB 예측 분석 엔진 v2.2 (시각화 모드)")

# 1. 모델 로드
@st.cache_resource
def load_model():
    return joblib.load('mlb_model.pkl')

if not os.path.exists('mlb_model.pkl'):
    st.error("모델 파일(mlb_model.pkl)을 찾을 수 없습니다. GitHub에 업로드했는지 확인하세요.")
else:
    model = load_model()

    # 2. 사용자 입력 변수 선언
    st.sidebar.header("데이터 입력")
    launch_angle = st.sidebar.number_input("Launch Angle", value=15.0)
    bat_speed = st.sidebar.number_input("Bat Speed", value=70.0)
    release_speed = st.sidebar.number_input("Release Speed", value=90.0)
    hyper_speed = st.sidebar.number_input("Hyper Speed", value=100.0)
    release_extension = st.sidebar.number_input("Release Extension", value=6.0)

    # 3. 예측 및 시각화 버튼
    if st.button("안타 확률 예측 및 시각화"):
        # 입력된 변수들로 DataFrame 생성
        input_data = [[launch_angle, bat_speed, release_speed, hyper_speed, release_extension]]
        cols = ['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension']
        input_df = pd.DataFrame(input_data, columns=cols)
        
        # 확률 계산
        proba = model.predict_proba(input_df)[0][1]
        
        # 4. 확률 시각화
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = proba * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "안타 확률 (%)"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}},
        ))
        st.plotly_chart(fig)
