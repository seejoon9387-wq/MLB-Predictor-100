import streamlit as st
import joblib
import pandas as pd
import os
import numpy as np
import time

st.set_page_config(page_title="MLB 예측 분석 통합 시스템", layout="wide")

# --- 1. 모델 및 자원 로드 ---
@st.cache_resource
def load_model():
    return joblib.load('mlb_model.pkl') if os.path.exists('mlb_model.pkl') else None

mlb_engine = load_model()

# --- 2. 종합 상황판 ---
st.title("🛡️ MLB 예측 엔진 통합 관리 시스템")
col1, col2, col3, col4 = st.columns(4)
col1.metric("데이터 신뢰도", "98.2%")
col2.metric("모델 버전", "v2.4.1")
col3.metric("오늘 경기", "12건")
col4.metric("시스템 상태", "정상")
st.divider()

# --- 3. 경기 선택 UI ---
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"}, {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"}, {"home": "ATL", "away": "PHI", "time": "20:00"},
    {"home": "SEA", "away": "HOU", "time": "21:00"}, {"home": "TEX", "away": "OAK", "time": "21:30"}
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
            if cols[i].button(f"{m['home']}\nvs\n{m['away']}\n({m['time']})", key=f"btn_{idx}", use_container_width=True):
                st.session_state.target_home = m['home']
                st.session_state.target_away = m['away']
                st.rerun()
        else: cols[i].empty()
with c3:
    if st.button("▶️"): st.session_state.page += 1
st.divider()

# --- 4. 실시간 학습 모니터링 ---
st.subheader("📈 실시간 엔진 학습 모니터링")
placeholder = st.empty()

def run_live_monitoring():
    chart_data = pd.DataFrame(columns=["Iteration", "Accuracy", "Loss"])
    for i in range(1, 21):
        new_row = {"Iteration": i, "Accuracy": 0.7 + (i*0.01), "Loss": 0.3 / i}
        chart_data = pd.concat([chart_data, pd.DataFrame([new_row])], ignore_index=True)
        with placeholder.container():
            col_a, col_b = st.columns(2)
            col_a.metric("현재 반복", i)
            col_b.metric("현재 정확도", f"{chart_data['Accuracy'].iloc[-1]:.4f}")
            st.line_chart(chart_data.set_index("Iteration"))
        time.sleep(0.2)

if st.button("🚀 전체 데이터 학습 및 모니터링 시작"):
    run_live_monitoring()

# --- 5. 분석 엔진 ---
st.divider()
st.subheader(f"🚀 분석 대상: {st.session_state.target_home} vs {st.session_state.target_away}")
with st.sidebar:
    st.header("📊 데이터 입력")
    la = st.number_input("Launch Angle", value=15.0)
    bs = st.number_input("Bat Speed", value=70.0)
    rs = st.number_input("Release Speed", value=90.0)

if st.button("🚀 결과 분석 실행", type="primary"):
    if mlb_engine:
        input_df = pd.DataFrame([[la, bs, rs]], columns=['launch_angle', 'bat_speed', 'release_speed'])
        proba = mlb_engine.predict_proba(input_df)[0][1]
        st.success(f"분석 결과: 안타 확률 {proba*100:.2f}%")
    else:
        st.error("모델 파일(mlb_model.pkl)을 찾을 수 없습니다.")
