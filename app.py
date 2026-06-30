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

# 2. 실시간 경기 데이터 (이 리스트에 데이터를 넣으면 개수에 맞춰 자동으로 생성됩니다)
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"}, 
    {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"}, 
    {"home": "ATL", "away": "PHI", "time": "20:00"}
    # 데이터가 4개라면, 박스도 4개만 생성됩니다.
]

if 'page' not in st.session_state: st.session_state.page = 0
items_per_page = 6

st.title("⚾ MLB 예측 분석 엔진")
st.subheader("🗓️ 경기 일정")

# 3. 레이아웃 고정
c_left, c_mid, c_right = st.columns([0.5, 11, 0.5])

with c_left:
    if st.button("◀️"): st.session_state.page = max(0, st.session_state.page - 1)

with c_mid:
    # 6개 고정 컬럼 생성
    cols = st.columns(6)
    start_idx = st.session_state.page * items_per_page
    
    # 데이터가 있는 만큼만 루프를 돕니다.
    for i in range(items_per_page):
        data_idx = start_idx + i
        with cols[i]:
            if data_idx < len(matches):
                match = matches[data_idx]
                with st.container(border=True):
                    st.markdown(f"**{match['home']}**")
                    st.write("vs")
                    st.markdown(f"**{match['away']}**")
                    st.caption(f"{match['time']}")
                    if st.button("선택", key=f"btn_{data_idx}", use_container_width=True):
                        st.session_state.target_home = match['home']
                        st.session_state.target_away = match['away']
                        st.rerun()
            else:
                # 데이터가 없으면 빈 공간으로 유지 (디자인 무너짐 방지)
                st.write("")

with c_right:
    # 페이지 최대값 설정 (데이터 개수 기준)
    max_pages = (len(matches) - 1) // items_per_page
    if st.button("▶️"): st.session_state.page = min(max_pages, st.session_state.page + 1)

# 4. 분석 연동 로직
if 'target_home' not in st.session_state: 
    st.session_state.target_home = matches[0]['home'] if matches else "Team"
    st.session_state.target_away = matches[0]['away'] if matches else "Team"

st.divider()
st.info(f"현재 선택된 경기: {st.session_state.target_home} vs {st.session_state.target_away}")
