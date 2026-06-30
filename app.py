import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import os

# 페이지 설정
st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

st.title("⚾ MLB 예측 분석 엔진 v2.2 (통합 분석 모드)")

# 1. 모델 로드 (에러 핸들링 포함)
@st.cache_resource
def load_model():
    try:
        return joblib.load('mlb_model.pkl')
    except Exception as e:
        st.error(f"모델을 로드하는 중 오류 발생: {e}")
        return None

# 2. 메인 실행 로직
model = load_model()

if model:
    # 3. 사용자 입력 사이드바 (데이터 타입을 명시적으로 지정)
    st.sidebar.header("타구 데이터 입력")
    try:
        launch_angle = st.sidebar.number_input("Launch Angle", value=15.0, step=0.1)
        bat_speed = st.sidebar.number_input("Bat Speed", value=70.0, step=0.1)
        release_speed = st.sidebar.number_input("Release Speed", value=90.0, step=0.1)
        hyper_speed = st.sidebar.number_input("Hyper Speed", value=100.0, step=0.1)
        release_extension = st.sidebar.number_input("Release Extension", value=6.0, step=0.1)
    except Exception as e:
        st.sidebar.error("입력값을 확인하세요.")

    # 4. 예측 실행
    if st.button("안타 확률 예측 및 분석"):
        input_data = pd.DataFrame([[launch_angle, bat_speed, release_speed, hyper_speed, release_extension]], 
                                  columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
        
        # 확률 계산
        proba = model.predict_proba(input_data)[0][1]
        
        # 5. 확률 게이지 시각화
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = proba * 100,
            title = {'text': "예측 안타 확률 (%)"},
            gauge = {'axis': {'range': [0, 100]}, 
                     'bar': {'color': "darkblue"},
                     'steps': [{'range': [0, 30], 'color': "lightgray"}, {'range': [30, 70], 'color': "skyblue"}]}
        ))
        st.plotly_chart(fig, use_container_width=True)

    # 6. 데이터 분포 시각화
    st.divider()
    st.subheader("데이터 분포 분석")
    if os.path.exists('data_sample.csv'):
        if st.checkbox("학습 데이터 분포 산점도 보기"):
            df_sample = pd.read_csv('data_sample.csv')
            
            fig_scatter = go.Figure()
            for result, color in zip([0, 1], ["red", "green"]):
                subset = df_sample[df_sample['hit_binary'] == result]
                fig_scatter.add_trace(go.Scatter(
                    x=subset['launch_angle'], 
                    y=subset['launch_speed'],
                    mode='markers', 
                    name='안타' if result == 1 else '범타',
                    marker=dict(color=color, opacity=0.5)
                ))
            
            fig_scatter.update_layout(title="타구 속도 vs 발사 각도", xaxis_title="발사 각도", yaxis_title="타구 속도")
            st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("데이터 샘플(data_sample.csv)을 프로젝트 폴더에 업로드하세요.")
else:
    st.error("시스템을 구동하기 위한 모델 파일을 찾을 수 없습니다.")import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import os

# 페이지 설정
st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

st.title("⚾ MLB 예측 분석 엔진 v2.2 (통합 분석 모드)")

# 1. 모델 로드 (에러 핸들링 포함)
@st.cache_resource
def load_model():
    try:
        return joblib.load('mlb_model.pkl')
    except Exception as e:
        st.error(f"모델을 로드하는 중 오류 발생: {e}")
        return None

# 2. 메인 실행 로직
model = load_model()

if model:
    # 3. 사용자 입력 사이드바 (데이터 타입을 명시적으로 지정)
    st.sidebar.header("타구 데이터 입력")
    try:
        launch_angle = st.sidebar.number_input("Launch Angle", value=15.0, step=0.1)
        bat_speed = st.sidebar.number_input("Bat Speed", value=70.0, step=0.1)
        release_speed = st.sidebar.number_input("Release Speed", value=90.0, step=0.1)
        hyper_speed = st.sidebar.number_input("Hyper Speed", value=100.0, step=0.1)
        release_extension = st.sidebar.number_input("Release Extension", value=6.0, step=0.1)
    except Exception as e:
        st.sidebar.error("입력값을 확인하세요.")

    # 4. 예측 실행
    if st.button("안타 확률 예측 및 분석"):
        input_data = pd.DataFrame([[launch_angle, bat_speed, release_speed, hyper_speed, release_extension]], 
                                  columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
        
        # 확률 계산
        proba = model.predict_proba(input_data)[0][1]
        
        # 5. 확률 게이지 시각화
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = proba * 100,
            title = {'text': "예측 안타 확률 (%)"},
            gauge = {'axis': {'range': [0, 100]}, 
                     'bar': {'color': "darkblue"},
                     'steps': [{'range': [0, 30], 'color': "lightgray"}, {'range': [30, 70], 'color': "skyblue"}]}
        ))
        st.plotly_chart(fig, use_container_width=True)

    # 6. 데이터 분포 시각화
    st.divider()
    st.subheader("데이터 분포 분석")
    if os.path.exists('data_sample.csv'):
        if st.checkbox("학습 데이터 분포 산점도 보기"):
            df_sample = pd.read_csv('data_sample.csv')
            
            fig_scatter = go.Figure()
            for result, color in zip([0, 1], ["red", "green"]):
                subset = df_sample[df_sample['hit_binary'] == result]
                fig_scatter.add_trace(go.Scatter(
                    x=subset['launch_angle'], 
                    y=subset['launch_speed'],
                    mode='markers', 
                    name='안타' if result == 1 else '범타',
                    marker=dict(color=color, opacity=0.5)
                ))
            
            fig_scatter.update_layout(title="타구 속도 vs 발사 각도", xaxis_title="발사 각도", yaxis_title="타구 속도")
            st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("데이터 샘플(data_sample.csv)을 프로젝트 폴더에 업로드하세요.")
else:
    st.error("시스템을 구동하기 위한 모델 파일을 찾을 수 없습니다.")
