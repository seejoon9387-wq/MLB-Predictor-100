import streamlit as st
import joblib
import pandas as pd
import os

st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

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

# 페이지 상태
if 'page' not in st.session_state: st.session_state.page = 0

st.title("⚾ MLB 예측 분석 엔진")

# 화살표 및 박스 레이아웃
c1, c2, c3 = st.columns([1, 10, 1])

with c1:
    if st.button("◀️"): st.session_state.page = max(0, st.session_state.page - 1)

with c2:
    cols = st.columns(6)
    start_idx = st.session_state.page * 6
    
    for i in range(6):
        idx = start_idx + i
        if idx < len(matches):
            m = matches[idx]
            # 버튼 텍스트를 이용해 박스 형태 유지
            label = f"{m['home']}\nvs\n{m['away']}\n({m['time']})"
            if cols[i].button(label, key=f"btn_{idx}", use_container_width=True):
                st.session_state.target_home = m['home']
                st.session_state.target_away = m['away']
                st.rerun()
        else:
            cols[i].empty()

with c3:
    if st.button("▶️"): st.session_state.page += 1

# 분석 대상 정보
if 'target_home' not in st.session_state: 
    st.session_state.target_home = matches[0]['home']
    st.session_state.target_away = matches[0]['away']

st.divider()
st.subheader(f"현재 선택된 경기: {st.session_state.target_home} vs {st.session_state.target_away}")
