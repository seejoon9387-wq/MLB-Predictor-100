import streamlit as st
import pandas as pd
import joblib
import os

# 페이지 설정
st.set_page_config(page_title="MLB 분석 엔진", layout="wide")

st.title("🛡️ MLB 예측 엔진 통합 관리 시스템")

# 1. 모델 및 데이터 로드 함수
@st.cache_resource
def load_model():
    return joblib.load('mlb_model.pkl')

@st.cache_data
def load_data():
    # 깃허브에는 전체 데이터(1.4GB)를 올리지 말고, 
    # 분석용으로 가공된 작은 샘플 데이터를 활용하세요.
    return pd.read_csv("mlb_master_final.csv")

# 모델 초기화
try:
    model = load_model()
    st.sidebar.success("모델 로드 성공: v2.4.1")
except:
    st.sidebar.error("모델 파일을 찾을 수 없습니다.")

# 2. 메인 로직
st.write("---")
# 경기 날짜 선택
selected_date = st.date_input("🗓️ 분석할 경기 날짜를 선택하세요")

# 데이터 처리
if os.path.exists("mlb_master_final.csv"):
    df = load_data()
    # 날짜 필터링
    df['game_date'] = pd.to_datetime(df['game_date'])
    filtered_df = df[df['game_date'].dt.date == selected_date]

    if not filtered_df.empty:
        st.write(f"🔍 {selected_date} 경기 목록")
        game_list = filtered_df['game_pk'].unique()
        selected_game = st.selectbox("분석할 경기 선택", game_list)
        
        # 분석 버튼
        if st.button("🚀 분석 실행"):
            # 분석용 피처 선택
            features = ['launch_angle', 'bat_speed', 'release_speed', 'plate_x', 'plate_z', 'spin_axis']
            data_to_predict = filtered_df[filtered_df['game_pk'] == selected_game][features].fillna(0)
            
            # 예측 실행
            prob = model.predict_proba(data_to_predict.iloc[0:1])[0][1]
            
            # 결과 출력
            st.metric(label="안타 확률", value=f"{prob*100:.2f}%")
            st.progress(float(prob))
    else:
        st.warning("해당 날짜에 분석 가능한 데이터가 없습니다.")
else:
    st.error("데이터 파일(mlb_master_final.csv)이 업로드되지 않았습니다.")
