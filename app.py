import streamlit as st
import joblib
import pandas as pd
import os

st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

# 모델 로드
def load_model():
    return joblib.load('mlb_model.pkl') if os.path.exists('mlb_model.pkl') else None
model = load_model()

# 경기 데이터 (6개 경기)
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"}, {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"}, {"home": "ATL", "away": "PHI", "time": "20:00"},
    {"home": "SEA", "away": "HOU", "time": "21:00"}, {"home": "TEX", "away": "OAK", "time": "21:30"}
]

if 'page' not in st.session_state: st.session_state.page = 0

st.title("⚾ MLB 예측 분석 엔진")
st.subheader("🗓️ 경기 일정 (클릭하여 선택)")

# 화살표와 6개 박스 배치를 위한 레이아웃
c_left, c_mid, c_right = st.columns([0.5, 11, 0.5])

with c_left:
    if st.button("◀️"): st.session_state.page = max(0, st.session_state.page - 1)

with c_mid:
    # 6개 박스를 위한 컬럼 생성
    cols = st.columns(6)
    
    for i, col in enumerate(cols):
        # 각 컬럼 안에 박스 역할을 할 컨테이너 생성
        with col:
            with st.container(border=True): # border=True가 핵심: 박스 테두리 생성
                match = matches[i]
                # 박스 내부 정보 표시
                st.markdown(f"**{match['home']}**")
                st.write("vs")
                st.markdown(f"**{match['away']}**")
                st.caption(f"{match['time']}")
                
                # 클릭 버튼 (데이터 연동)
                if st.button("분석 선택", key=f"btn_{i}", use_container_width=True):
                    st.session_state.target_home = match['home']
                    st.session_state.target_away = match['away']
                    st.rerun()

with c_right:
    if st.button("▶️"): st.session_state.page = min(1, st.session_state.page + 1)

# 분석 로직
if 'target_home' not in st.session_state: 
    st.session_state.target_home = matches[0]['home']
    st.session_state.target_away = matches[0]['away']

st.divider()
st.info(f"현재 선택된 경기: {st.session_state.target_home} vs {st.session_state.target_away}")

# (기존 입력/분석 로직 동일)
