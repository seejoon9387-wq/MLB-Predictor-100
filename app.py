import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import os

# 페이지 설정
st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

# 1. 모델 로드
@st.cache_resource
def load_model():
    return joblib.load('mlb_model.pkl') if os.path.exists('mlb_model.pkl') else None

model = load_model()

# 2. 메인 UI 및 캐러셀
st.title("⚾ MLB 예측 분석 엔진 v2.2")
st.subheader("🗓️ 실시간 경기 일정")

# 경기 데이터 (6개 팀 / 3경기)
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"},
    {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"},
    {"home": "ATL", "away": "PHI", "time": "20:00"},
    {"home": "SEA", "away": "HOU", "time": "21:00"},
    {"home": "TEX", "away": "OAK", "time": "21:30"}
]

# 디자인을 위한 CSS 삽입 (음영과 테두리)
st.markdown("""
    <style>
    .match-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        background-color: #f9f9f9;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 페이지네이션 관리
if 'page' not in st.session_state: st.session_state.page = 0

col_left, col_mid, col_right = st.columns([1, 10, 1])

with col_mid:
    # 6개 팀을 3개씩 보여주기 (슬라이더)
    current_matches = matches[st.session_state.page*3 : (st.session_state.page+1)*3]
    
    cols = st.columns(3)
    for i, match in enumerate(current_matches):
        with cols[i]:
            st.markdown(f"""
                <div class="match-card">
                    <b>{match['home']} vs {match['away']}</b><br>
                    <span>{match['time']}</span>
                </div>
            """, unsafe_allow_html=True)

with col_left:
    if st.button("◀️"): st.session_state.page = max(0, st.session_state.page - 1)
with col_right:
    if st.button("▶️"): st.session_state.page = min((len(matches)//3)-1, st.session_state.page + 1)

# 3. 사이드바 입력 및 분석
st.sidebar.header("📊 입력 컨트롤러")
home_team = st.sidebar.text_input("홈 팀", value="Home Team")
away_team = st.sidebar.text_input("원정 팀", value="Away Team")

launch_angle = st.sidebar.number_input("Launch Angle", value=15.0, step=0.1)
bat_speed = st.sidebar.number_input("Bat Speed", value=70.0, step=0.1)
release_speed = st.sidebar.number_input("Release Speed", value=90.0, step=0.1)
hyper_speed = st.sidebar.number_input("Hyper Speed", value=100.0, step=0.1)
release_extension = st.sidebar.number_input("Release Extension", value=6.0, step=0.1)

if st.button("🚀 결과 분석 실행", type="primary"):
    if not model:
        st.error("모델 파일을 찾을 수 없습니다.")
    else:
        input_data = pd.DataFrame([[launch_angle, bat_speed, release_speed, hyper_speed, release_extension]], 
                                  columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
        proba = model.predict_proba(input_data)[0][1]
        
        st.subheader(f"결과: {home_team} vs {away_team}")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number", value = proba * 100, title = {'text': "안타 확률 (%)"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#1f77b4"}}
        ))
        st.plotly_chart(fig, use_container_width=True)
