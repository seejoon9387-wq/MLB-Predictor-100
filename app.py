import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go # 시각화 라이브러리 추가

# 모델 로드 (생략)
model = joblib.load('mlb_model.pkl')

st.title("MLB 예측 분석 엔진 v2.2 (시각화 모드)")

# 입력 (생략)
# ... [이전 입력 코드와 동일] ...

if st.button("안타 확률 예측 및 시각화"):
    input_df = pd.DataFrame([[launch_angle, bat_speed, release_speed, hyper_speed, release_extension]], 
                              columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
    
    proba = model.predict_proba(input_df)[0][1]
    
    # 확률 시각화 (게이지 차트)
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = proba * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "안타 확률 (%)"},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}},
    ))
    st.plotly_chart(fig)
