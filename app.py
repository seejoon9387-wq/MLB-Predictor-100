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

# 2. 경기 데이터 (예시: 12개 경기 데이터)
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"}, {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"}, {"home": "ATL", "away": "PHI", "time": "20:00"},
    {"home": "SEA", "away": "HOU", "time": "21:00"}, {"home": "TEX", "away": "OAK", "time": "21:30"},
    {"home": "BAL", "away": "TOR", "time": "18:00"}, {"home": "CLE", "away": "DET", "time": "18:30"},
    {"home": "MIN", "away": "CWS", "time": "19:00"}, {"home": "KC", "away": "LAA", "time": "19:30"},
    {"home": "NYM", "away": "MIA", "time": "20:00"}, {"home": "WSH", "away": "PIT", "time": "20:30"}
]

# 페이지 상태 관리
if 'page' not in st.session_state: st.session_state.page = 0
items_per_page = 6
max_pages = (len(matches) - 1) // items_per_page

st.title("⚾ MLB 예측 분석 엔진")
st.subheader("🗓️ 경기 일정 (화살표로 페이지 이동)")

# 3. 레이아웃 고정 및 데이터 렌더링
c_left, c_mid, c_right = st.columns([1, 10, 1])

with c_left:
    if st.button("◀️ 이전"): st.session_state.page = max(0, st.session_state.page - 1)

with c_mid:
    # 6개 경기씩 슬라이싱
    start_idx = st.session_state.page * items_per_page
    current_view = matches[start_idx : start_idx + items_per_page]
    
    # 2행 3열 배치를 위한 이중 루프
    for row in range(0, len(current_view), 3):
        cols = st.columns(3)
        for i, col in enumerate(cols):
            idx = row + i
            if idx < len(current_view):
                m = current_view[idx]
                # 버튼을 클릭하면 세션 데이터 업데이트
                if col.button(f"{m['home']} vs {m['away']}\n({m['time']})", key=f"match_{start_idx + idx}"):
                    st.session_state.target_home = m['home']
                    st.session_state.target_away = m['away']
                    st.rerun()

with c_right:
    if st.button("다음 ▶️"): st.session_state.page = min(max_pages, st.session_state.page + 1)

# 4. 분석 실행 영역
st.divider()
if 'target_home' not in st.session_state: st.session_state.target_home = matches[0]['home']
if 'target_away' not in st.session_state: st.session_state.target_away = matches[0]['away']

st.sidebar.header("📊 분석 데이터")
home = st.sidebar.text_input("홈 팀", value=st.session_state.target_home)
away = st.sidebar.text_input("원정 팀", value=st.session_state.target_away)

# (나머지 입력 필드들...)

if st.button("🚀 결과 분석 실행", type="primary"):
    st.write(f"분석 시작: {home} vs {away}")
