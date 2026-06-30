import streamlit as st
import joblib
import pandas as pd

st.title("MLB 예측 분석 엔진 v2.0 (Stable Model)")

# 1. GitHub에 올린 모델 로드
@st.cache_resource
def load_model():
    return joblib.load('mlb_model.pkl')

try:
    model = load_model()
    st.success("모델 로드 성공!")
except Exception as e:
    st.error(f"모델 로드 실패: {e}. 'mlb_model.pkl' 파일을 GitHub에 올렸는지 확인하세요.")

# 2. 예측 UI
st.sidebar.header("데이터 입력")
launch_angle = st.sidebar.number_input("Launch Angle", value=15.0)
bat_speed = st.sidebar.number_input("Bat Speed", value=70.0)
release_speed = st.sidebar.number_input("Release Speed", value=90.0)
hyper_speed = st.sidebar.number_input("Hyper Speed", value=100.0)
release_extension = st.sidebar.number_input("Release Extension", value=6.0)

if st.button("안타 확률 예측"):
    input_df = pd.DataFrame([[launch_angle, bat_speed, release_speed, hyper_speed, release_extension]], 
                              columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
    
    proba = model.predict_proba(input_df)[0][1]
    st.write(f"### 예측된 안타 확률: {proba*100:.2f}%")
