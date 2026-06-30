import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

# CSS는 한번만 로드되도록 설정
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
    </style>
""", unsafe_allow_html=True)

# 모델 로드
@st.cache_resource
def load_model():
    return joblib.load('mlb_model.pkl') if os.path.exists('mlb_model.pkl') else None

model = load_model()

# 경기 데이터
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"}, {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"}, {"home": "ATL", "away": "PHI", "time": "20:00"},
    {"home": "SEA", "away": "HOU", "time": "21:00"}, {"home": "TEX", "away": "OAK", "time": "21:30"}
]

# 페이지네이션 초기화
if 'page' not in st.session_state: st.session_state.page = 0

st.title("⚾ MLB 예측 분석 엔진 v2.2")
st.subheader("🗓️ 실시간 경기 일정")

# [핵심 수정] 박스 렌더링 영역을 명확히 구분
container = st.container()
with container:
    col_left, col_mid, col_right = st.columns([1, 10, 1])
    
    with col_mid:
        current_matches = matches[st.session_state.page*6 : (st.session_state.page+1)*6]
        # 박스가 없으면 메시지라도 출력하여 확인
        if not current_matches:
            st.write("표시할 일정이 없습니다.")
        else:
            for row in range(0, len(current_matches), 3):
                cols = st.columns(3)
                for i, match in enumerate(current_matches[row:row+3]):
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
        if st.button("▶️"): st.session_state.page = min((len(matches)//6), st.session_state.page + 1)

# 사이드바 및 분석 코드(생략)
# ... (이후 동일하게 유지)
