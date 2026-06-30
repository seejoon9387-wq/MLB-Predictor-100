import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import os

# 페이지 설정
st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

st.title("⚾ MLB 예측 분석 엔진 v2.2 (통합 분석 모드)")

# 1. 모델 로드 (캐시 사용)
@st.cache_resource
def load_model():
    try:
        if os.path.exists('mlb_model.pkl'):
            return joblib.load('mlb_model.pkl')
        else:
            return None
    except Exception as e:
        st.error(f"모델 로드 오류: {e}")
        return None

# 모델 불러오기
model = load_model()

# 2. 메인 로직
if model is None:
    st.error("시스템을 구동하기 위한 모델 파일(mlb_model.pkl)을 찾을 수 없습니다.")
else:
    # 3. 사이드바 입력
    st.sidebar.header("타구 데이터 입력")
    launch_angle = st.sidebar.number_input("Launch Angle", value=15.0, step=0.1)
    bat_speed = st.sidebar.number_input("Bat Speed", value=70.0, step=0.1)
    release_speed = st.sidebar.number_input("Release Speed", value=90.0, step=0.1)
    hyper_speed = st.sidebar.number_input("Hyper Speed", value=100.0, step=0.1)
    release_extension = st.sidebar.number_input("Release Extension", value=6.0, step=0.1)

    # 4. 예측 실행
    if st.button("안타 확률 예측 및 분석"):
        input_data = pd.DataFrame([[launch_angle, bat_speed, release_speed, hyper_speed, release_extension]], 
                                  columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
        
        proba = model.predict_proba(input_data)[0][1]
        
        # 5. 확률 게이지
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = proba * 100,
            title = {'text': "예측 안타 확률 (%)"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
        ))
        st.plotly_chart(fig, use_container_width=True)

    # 6. 데이터 분포
    st.divider()
    st.subheader("데이터 분포 분석")
    if os.path.exists('data_sample.csv'):
        if st.checkbox("학습 데이터 분포 산점도 보기"):
            df_sample = pd.read_csv('data_sample.csv')
            fig_scatter = go.Figure()
            # 'launch_speed' 컬럼이 데이터에 존재하는지 확인
            y_col = 'launch_speed' if 'launch_speed' in df_sample.columns else 'bat_speed'
            
            for result, color in zip([0, 1], ["red", "green"]):
                subset = df_sample[df_sample['hit_binary'] == result]
                fig_scatter.add_trace(go.Scatter(
                    x=subset['launch_angle'], y=subset[y_col],
                    mode='markers', name='안타' if result == 1 else '범타',
                    marker=dict(color=color, opacity=0.5)
                ))
            st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("분석할 데이터 샘플(data_sample.csv)을 폴더에 추가하세요.")

# [파일: app.py] 수정된 부분
# ... (상단 코드 생략)

    # 3. 사이드바 입력
    st.sidebar.header("경기 및 타구 데이터 입력")
    
    # 팀 이름 입력창 추가
    home_team = st.sidebar.text_input("홈 팀 이름", value="Home Team")
    away_team = st.sidebar.text_input("원정 팀 이름", value="Away Team")
    
    st.sidebar.divider() # 구분선 추가
    
    launch_angle = st.sidebar.number_input("Launch Angle", value=15.0, step=0.1)
    # ... (이하 나머지 입력값 동일)

    # 4. 예측 실행
    if st.button("안타 확률 예측 및 분석"):
        st.subheader(f"경기 분석: {home_team} vs {away_team}") # 입력된 팀 이름 표시
        input_data = pd.DataFrame([[launch_angle, bat_speed, release_speed, hyper_speed, release_extension]], 
                                  columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
        # ... (이하 동일)
