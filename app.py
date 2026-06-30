import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import os

st.title("MLB 예측 분석 엔진 v2.2 (통합 분석 모드)")

# 1. 모델 및 데이터 로드 (캐시 사용으로 서버 부하 방지)
@st.cache_resource
def load_model():
    return joblib.load('mlb_model.pkl')

# 2. 모델 파일 및 데이터 파일 확인
if not os.path.exists('mlb_model.pkl'):
    st.error("모델 파일(mlb_model.pkl)을 찾을 수 없습니다.")
else:
    model = load_model()
    
    # 3. 사용자 입력 사이드바
    st.sidebar.header("타구 데이터 입력")
    launch_angle = st.sidebar.number_input("Launch Angle", value=15.0)
    bat_speed = st.sidebar.number_input("Bat Speed", value=70.0)
    release_speed = st.sidebar.number_input("Release Speed", value=90.0)
    hyper_speed = st.sidebar.number_input("Hyper Speed", value=100.0)
    release_extension = st.sidebar.number_input("Release Extension", value=6.0)

    # 4. 예측 실행 버튼
    if st.button("안타 확률 예측 및 분석"):
        # 입력 데이터 생성
        input_data = [[launch_angle, bat_speed, release_speed, hyper_speed, release_extension]]
        cols = ['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension']
        input_df = pd.DataFrame(input_data, columns=cols)
        
        # 확률 계산
        proba = model.predict_proba(input_df)[0][1]
        
        # 5. 확률 게이지 시각화
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = proba * 100,
            title = {'text': "안타 확률 (%)"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
        ))
        st.plotly_chart(fig)

    # 6. 데이터 분포 시각화 (산점도)
    st.divider()
    st.subheader("데이터 분포 분석")
    if os.path.exists('data_sample.csv'):
        if st.checkbox("학습 데이터 분포 산점도 보기"):
            df_sample = pd.read_csv('data_sample.csv')
            
            fig_scatter = go.Figure()
            for result in [0, 1]:
                subset = df_sample[df_sample['hit_binary'] == result]
                fig_scatter.add_trace(go.Scatter(
                    x=subset['launch_angle'], y=subset['launch_speed'],
                    mode='markers', name='안타' if result == 1 else '범타',
                    opacity=0.5
                ))
            
            fig_scatter.update_layout(title="타구 속도 vs 발사 각도", xaxis_title="발사 각도", yaxis_title="타구 속도")
            st.plotly_chart(fig_scatter)
    else:
        st.warning("분석할 데이터 샘플(data_sample.csv)을 GitHub에 업로드하세요.")
