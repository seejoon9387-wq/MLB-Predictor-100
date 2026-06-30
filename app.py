import streamlit as st
import joblib
import pandas as pd
import os

st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

# 모델 로드
def load_model():
    return joblib.load('mlb_model.pkl') if os.path.exists('mlb_model.pkl') else None
model = load_model()

# 경기 데이터
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"}, {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"}, {"home": "ATL", "away": "PHI", "time": "20:00"},
    {"home": "SEA", "away": "HOU", "time": "21:00"}, {"home": "TEX", "away": "OAK", "time": "21:30"},
    {"home": "BAL", "away": "TOR", "time": "18:00"}, {"home": "CLE", "away": "DET", "time": "18:30"}
]

# 상태 초기화
if 'page' not in st.session_state: st.session_state.page = 0
if 'target_home' not in st.session_state: st.session_state.target_home = matches[0]['home']
if 'target_away' not in st.session_state: st.session_state.target_away = matches[0]['away']

st.title("⚾ MLB 예측 분석 엔진")

# 레이아웃 구성
left_col, center_col, right_col = st.columns([1, 10, 1])

# 이전 페이지
with left_col:
    if st.button("◀️"):
        st.session_state.page = max(0, st.session_state.page - 1)

# 중앙 박스 배치
with center_col:
    cols = st.columns(6)
    start_idx = st.session_state.page * 6
    
    for i in range(6):
        idx = start_idx + i
        if idx < len(matches):
            match = matches[idx]
            # 버튼 내부에 정보를 모두 넣어 박스처럼 보이게 함 (가장 안정적)
            if cols[i].button(f"{match['home']}\nvs\n{match['away']}\n\n{match['time']}", key=f"btn_{idx}"):
                st.session_state.target_home = match['home']
                st.session_state.target_away = match['away']
                st.rerun()
        else:
            cols[i].empty() # 데이터 없으면 빈 칸 유지

# 다음 페이지
with right_col:
    if st.button("▶️"):
        st.session_state.page += 1

st.divider()
st.subheader(f"✅ 현재 선택된 경기: {st.session_state.target_home} vs {st.session_state.target_away}")

# 분석 실행 버튼
if st.button("🚀 결과 분석 실행", type="primary"):
    st.write("분석 엔진 가동 중...")
