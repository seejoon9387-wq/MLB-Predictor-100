import streamlit as st
import joblib
import pandas as pd
import os

st.set_page_config(page_title="MLB 예측 분석 통합 시스템", layout="wide")

# --- 1. 설정 및 모델 로드 ---
@st.cache_resource
def load_model():
    return joblib.load('mlb_model.pkl') if os.path.exists('mlb_model.pkl') else None

model = load_model()

# --- 2. 종합 상황판 (System Dashboard) ---
st.title("🛡️ MLB 예측 엔진 통합 관리 시스템")

col1, col2, col3, col4 = st.columns(4)
col1.metric("데이터 신뢰도", "98.2%")
col2.metric("모델 버전", "v2.4.1")
col3.metric("오늘 경기", "12건")
col4.metric("시스템 상태", "정상")

st.divider()

# --- 3. 경기 선택 UI (6개 박스 페이징) ---
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"}, {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"}, {"home": "ATL", "away": "PHI", "time": "20:00"},
    {"home": "SEA", "away": "HOU", "time": "21:00"}, {"home": "TEX", "away": "OAK", "time": "21:30"},
    {"home": "BAL", "away": "TOR", "time": "18:00"}, {"home": "CLE", "away": "DET", "time": "18:30"}
]

if 'page' not in st.session_state: st.session_state.page = 0
if 'target_home' not in st.session_state: st.session_state.target_home = matches[0]['home']
if 'target_away' not in st.session_state: st.session_state.target_away = matches[0]['away']

st.subheader("🗓️ 경기 일정 선택")
c1, c2, c3 = st.columns([0.5, 11, 0.5])

with c1:
    if st.button("◀️"): st.session_state.page = max(0, st.session_state.page - 1)

with c2:
    cols = st.columns(6)
    start_idx = st.session_state.page * 6
    for i in range(6):
        idx = start_idx + i
        if idx < len(matches):
            m = matches[idx]
            if cols[i].button(f"{m['home']}\nvs\n{m['away']}\n\n({m['time']})", key=f"btn_{idx}", use_container_width=True):
                st.session_state.target_home = m['home']
                st.session_state.target_away = m['away']
                st.rerun()
        else:
            cols[i].empty()

with c3:
    if st.button("▶️"): st.session_state.page += 1

# --- 4. 분석 엔진 및 입력 ---
st.divider()
st.subheader(f"🚀 분석 대상: {st.session_state.target_home} vs {st.session_state.target_away}")

with st.sidebar:
    st.header("📊 데이터 입력")
    la = st.number_input("Launch Angle", value=15.0)
    bs = st.number_input("Bat Speed", value=70.0)
    rs = st.number_input("Release Speed", value=90.0)
    hs = st.number_input("Hyper Speed", value=100.0)
    re = st.number_input("Release Extension", value=6.0)

if st.button("🚀 결과 분석 실행", type="primary"):
    if model:
        try:
            input_df = pd.DataFrame([[la, bs, rs, hs, re]], 
                                    columns=['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension'])
            proba = model.predict_proba(input_df)[0][1]
            st.success(f"분석 결과: 안타 확률 {proba*100:.2f}%")
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")
    else:
        st.error("모델 파일이 없습니다.")
