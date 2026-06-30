import streamlit as st
import joblib
import pandas as pd
import os

st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

# 1. 모델 로드
@st.cache_resource
def load_model():
    return joblib.load('mlb_model.pkl') if os.path.exists('mlb_model.pkl') else None

model = load_model()

# 2. 경기 데이터 (6개 경기씩 페이징)
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"}, {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"}, {"home": "ATL", "away": "PHI", "time": "20:00"},
    {"home": "SEA", "away": "HOU", "time": "21:00"}, {"home": "TEX", "away": "OAK", "time": "21:30"}
]

if 'page' not in st.session_state: st.session_state.page = 0
items_per_page = 6
max_pages = (len(matches) - 1) // items_per_page

st.title("⚾ MLB 예측 분석 엔진")
st.subheader("🗓️ 경기 일정 (한 줄 6경기 배치)")

# 3. 레이아웃: 1행 6열 (각 컬럼의 크기를 충분히 확보)
c_left, c_mid, c_right = st.columns([0.5, 11, 0.5])

with c_left:
    if st.button("◀️"): st.session_state.page = max(0, st.session_state.page - 1)

with c_mid:
    cols = st.columns(6) # 6개 컬럼 배치
    start_idx = st.session_state.page * items_per_page
    current_view = matches[start_idx : start_idx + items_per_page]
    
    for i, col in enumerate(cols):
        if i < len(current_view):
            m = current_view[i]
            # 클릭 가능한 카드 영역 생성
            with col:
                # 버튼을 통해 클릭 시 데이터 연동
                if st.button(f"{m['home']}\nvs\n{m['away']}\n\n{m['time']}", key=f"btn_{start_idx+i}", use_container_width=True):
                    st.session_state.target_home = m['home']
                    st.session_state.target_away = m['away']
                    st.rerun()

with c_right:
    if st.button("▶️"): st.session_state.page = min(max_pages, st.session_state.page + 1)

# 4. 분석 연동
if 'target_home' not in st.session_state: st.session_state.target_home = matches[0]['home']
if 'target_away' not in st.session_state: st.session_state.target_away = matches[0]['away']

st.divider()
st.write(f"### 분석 대상: **{st.session_state.target_home}** vs **{st.session_state.target_away}**")
