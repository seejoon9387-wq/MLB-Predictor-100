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

# 2. 디자인을 위한 CSS 삽입 (음영과 테두리)
st.markdown("""
    <style>
    .match-card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        background-color: #ffffff;
        margin: 10px;
    }
    .match-card b { font-size: 1.2em; }
    </style>
""", unsafe_allow_html=True)

# 3. 메인 UI 및 경기 일정 캐러셀
st.title("⚾ MLB 예측 분석 엔진 v2.2")
st.subheader("🗓️ 실시간 경기 일정")

# 경기 데이터 (12개 팀 / 6경기 예시)
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"}, {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"}, {"home": "ATL", "away": "PHI", "time": "20:00"},
    {"home": "SEA", "away": "HOU", "time": "21:00"}, {"home": "TEX", "away": "OAK", "time": "21:30"}
]

# 페이지네이션 (6개씩 처리)
if 'page' not in st.session_state: st.session_state.page = 0

col_left, col_mid, col_right = st.columns([1, 10, 1])

with col_mid:
    # 6개 경기 추출
    current_matches = matches[st.session_state.page*6 : (st.session_state.page+1)*6]
    
    # 2행 3열 배치를 위한 이중 루프
    for row in range(0, len(current_matches), 3):
        cols = st.columns(3)
        for i, match in enumerate(current_matches[row:row+3]):
            with cols[i]:
                st.markdown(f"""
                    <div class="match-card">
                        <b>{match['home']} vs {match['away']}</b><br>
                        <span>시작 시간: {match['time']}</span>
                    </div>
                """, unsafe_allow_html=True)

with col_left:
    if st.button("◀️"): st.session_state.page = max(0, st.session_state.page - 1)
with col_right:
    if st.button("▶️"): st.session_state.page = min((len(matches)//6), st.session_state.page + 1)

# 4. 사이드바: 입력 컨트롤러
st.sidebar.header("📊 데이터 입력")
home_team = st.sidebar.text_input("홈 팀", value="Home Team")
away_team = st.sidebar.text_input("원정 팀", value="Away Team")
launch_angle = st.sidebar.number_input("Launch Angle", value=15.0, step=0.1)
bat_speed = st.sidebar.number_input("Bat Speed", value=70.0, step=0.1)
release_speed = st.sidebar.number_input("Release Speed", value=90.0, step=0.1)
hyper_speed = st.sidebar.number_input("Hyper Speed", value=100.0, step=0.1)
release_extension = st.sidebar.number_input("Release Extension", value=6.0, step=0.1)

# 5. 분석 실행
st.divider()
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
