import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

# 1. 사이드바: 입력 영역
st.sidebar.header("📊 입력 컨트롤러")
home_team = st.sidebar.text_input("홈 팀", value="Home Team", key="home_input")
away_team = st.sidebar.text_input("원정 팀", value="Away Team", key="away_input")

st.sidebar.divider()
launch_angle = st.sidebar.number_input("Launch Angle", value=15.0, step=0.1, key="la")
bat_speed = st.sidebar.number_input("Bat Speed", value=70.0, step=0.1, key="bs")
release_speed = st.sidebar.number_input("Release Speed", value=90.0, step=0.1, key="rs")
hyper_speed = st.sidebar.number_input("Hyper Speed", value=100.0, step=0.1, key="hs")
release_extension = st.sidebar.number_input("Release Extension", value=6.0, step=0.1, key="re")

# 2. 메인: 분석 버튼 영역
st.title("⚾ MLB 예측 분석 엔진 v2.2")
st.info("좌측 패널에서 데이터를 입력한 후 아래 버튼을 클릭하여 분석을 시작하세요.")

# [결과 분석] 버튼
if st.button("🚀 결과 분석 실행", type="primary"):
    # 버튼이 눌렸을 때만 실행되는 블록
    with st.spinner('엔진 가동 중... 확률 계산 중입니다...'):
        if not os.path.exists('mlb_model.pkl'):
            st.error("오류: 모델 파일(mlb_model.pkl)을 찾을 수 없습니다.")
        else:
            model = joblib.load('mlb_model.pkl')
            input_data = pd.DataFrame([[launch_angle, bat_speed, release_speed, hyper_speed, release_extension]], 
                                      columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
            
            proba = model.predict_proba(input_data)[0][1]
            
            # 결과 출력
            st.subheader(f"결과: {home_team} vs {away_team}")
            
            # 시각화
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = proba * 100,
                title = {'text': "안타 확률 (%)"},
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#1f77b4"}}
            ))
            st.plotly_chart(fig, use_container_width=True)
            st.success("분석이 완료되었습니다.")
