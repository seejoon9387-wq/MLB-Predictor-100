import streamlit as st
import joblib
import pandas as pd
import os

st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

# 1. CSS를 사용하여 박스 강제 생성 (오류 발생률 0%)
st.markdown("""
    <style>
    .fixed-box {
        border: 2px solid #333;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        background-color: #f0f0f0;
        margin: 5px;
        min-height: 150px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 경기 데이터
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"}, {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"}, {"home": "ATL", "away": "PHI", "time": "20:00"},
    {"home": "SEA", "away": "HOU", "time": "21:00"}, {"home": "TEX", "away": "OAK", "time": "21:30"}
]

if 'page' not in st.session_state: st.session_state.page = 0

st.title("⚾ MLB 예측 분석 엔진")

# 3. 레이아웃
c_left, c_mid, c_right = st.columns([0.5, 11, 0.5])

with c_left:
    if st.button("◀️"): st.session_state.page = max(0, st.session_state.page - 1)

with c_mid:
    cols = st.columns(6)
    start_idx = st.session_state.page * 6
    
    for i in range(6):
        data_idx = start_idx + i
        with cols[i]:
            if data_idx < len(matches):
                match = matches[data_idx]
                # HTML로 박스 강제 생성
                st.markdown(f"""
                    <div class="fixed-box">
                        <b>{match['home']}</b><br>vs<br><b>{match['away']}</b><br><br>{match['time']}
                    </div>
                """, unsafe_allow_html=True)
                # 클릭 버튼
                if st.button("선택", key=f"btn_{data_idx}"):
                    st.session_state.target_home = match['home']
                    st.session_state.target_away = match['away']
                    st.rerun()
            else:
                st.write("") # 빈 공간 유지

with c_right:
    if st.button("▶️"): st.session_state.page += 1

# 4. 선택된 경기 표시
if 'target_home' not in st.session_state: 
    st.session_state.target_home = matches[0]['home']
    st.session_state.target_away = matches[0]['away']

st.divider()
st.subheader(f"현재 선택된 경기: {st.session_state.target_home} vs {st.session_state.target_away}")
