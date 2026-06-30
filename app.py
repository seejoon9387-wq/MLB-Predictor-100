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

# 2. 실시간 경기 일정 데이터 (실제 데이터 연동 시 이 리스트만 업데이트하면 됩니다)
data = {
    "날짜/시간": ["06-30 18:30", "06-30 19:00", "06-30 18:30", "06-30 20:00", "06-30 21:00", "06-30 21:30"],
    "홈 팀": ["LAD", "NYY", "CHC", "ATL", "SEA", "TEX"],
    "원정 팀": ["SF", "BOS", "MIL", "PHI", "HOU", "OAK"]
}
df_schedule = pd.DataFrame(data)

# 3. 메인 UI
st.title("⚾ MLB 예측 분석 엔진")

# 실시간 경기 일정 표시
st.subheader("🗓️ 실시간 경기 일정")
st.table(df_schedule)

# 경기 선택 및 데이터 연동
st.subheader("✅ 분석할 경기 선택")
selected_match = st.selectbox("일정에서 경기를 선택하세요:", df_schedule["홈 팀"] + " vs " + df_schedule["원정 팀"])

# 선택 시 자동으로 세션 상태 업데이트
if st.button("경기 정보 가져오기"):
    home_name = selected_match.split(" vs ")[0]
    away_name = selected_match.split(" vs ")[1]
    st.session_state.target_home = home_name
    st.session_state.target_away = away_name
    st.rerun()

# 4. 분석 입력 영역
if 'target_home' not in st.session_state: st.session_state.target_home = "LAD"
if 'target_away' not in st.session_state: st.session_state.target_away = "SF"

st.divider()
st.sidebar.header("📊 데이터 입력")
home = st.sidebar.text_input("홈 팀", value=st.session_state.target_home)
away = st.sidebar.text_input("원정 팀", value=st.session_state.target_away)

la = st.sidebar.number_input("Launch Angle", value=15.0)
bs = st.sidebar.number_input("Bat Speed", value=70.0)
rs = st.sidebar.number_input("Release Speed", value=90.0)
hs = st.sidebar.number_input("Hyper Speed", value=100.0)
re = st.sidebar.number_input("Release Extension", value=6.0)

# 5. 분석 실행
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
