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

# 2. 경기 일정 데이터 (15경기)
data = {
    "홈 팀": [f"Team{i}" for i in range(1, 16)],
    "원정 팀": [f"Team{i+1}" for i in range(1, 16)]
}
df = pd.DataFrame(data)

st.title("⚾ MLB 예측 분석 엔진")

# 3. 탭을 이용한 경기 일정 표시 (15경기를 5개씩 3개 탭으로 분할)
st.subheader("🗓️ 전체 경기 일정 (15경기)")
tab1, tab2, tab3 = st.tabs(["1~5경기", "6~10경기", "11~15경기"])

with tab1:
    st.table(df.iloc[0:5])
with tab2:
    st.table(df.iloc[5:10])
with tab3:
    st.table(df.iloc[10:15])

# 4. 분석할 경기 선택
st.subheader("✅ 경기 선택 및 분석")
match_list = [f"{row['홈 팀']} vs {row['원정 팀']}" for _, row in df.iterrows()]
selected = st.selectbox("분석할 경기를 선택하세요:", match_list)

if 'target_home' not in st.session_state: st.session_state.target_home = "Team1"
if 'target_away' not in st.session_state: st.session_state.target_away = "Team2"

if st.button("경기 정보 가져오기"):
    h, a = selected.split(" vs ")
    st.session_state.target_home = h
    st.session_state.target_away = a
    st.rerun()

# 5. 데이터 입력 영역
st.divider()
st.sidebar.header("📊 데이터 입력")
home = st.sidebar.text_input("홈 팀", value=st.session_state.target_home)
away = st.sidebar.text_input("원정 팀", value=st.session_state.target_away)

la = st.sidebar.number_input("Launch Angle", value=15.0)
bs = st.sidebar.number_input("Bat Speed", value=70.0)
rs = st.sidebar.number_input("Release Speed", value=90.0)
hs = st.sidebar.number_input("Hyper Speed", value=100.0)
re = st.sidebar.number_input("Release Extension", value=6.0)

# 6. 분석 실행
if st.button("🚀 결과 분석 실행", type="primary"):
    if model:
        input_data = pd.DataFrame([[la, bs, rs, hs, re]], 
                                  columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
        proba = model.predict_proba(input_data)[0][1]
        
        st.subheader(f"결과: {home} vs {away}")
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=proba * 100, title={'text': "안타 확률 (%)"},
            gauge={'axis': {'range': [0, 100]}}
        ))
        st.plotly_chart(fig)
    else:
        st.error("모델 파일(mlb_model.pkl)을 찾을 수 없습니다.")
