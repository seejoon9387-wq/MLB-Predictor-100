import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")

# 1. 고정 스타일 (디자인 최소화, 박스 크기 확대)
st.markdown("""
    <style>
    div[data-testid="stColumn"] {
        background-color: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 5px;
        min-height: 180px; /* 박스 높이 키움 */
    }
    </style>
""", unsafe_allow_html=True)

# 2. 데이터 (예시)
matches = [
    {"home": "LAD", "away": "SF", "time": "18:30"}, {"home": "NYY", "away": "BOS", "time": "19:00"},
    {"home": "CHC", "away": "MIL", "time": "18:30"}, {"home": "ATL", "away": "PHI", "time": "20:00"},
    {"home": "SEA", "away": "HOU", "time": "21:00"}, {"home": "TEX", "away": "OAK", "time": "21:30"}
]

if 'page' not in st.session_state: st.session_state.page = 0

st.title("⚾ MLB 예측 분석 엔진")

# 3. 레이아웃 (반응 속도 개선을 위해 컨테이너 직접 배치)
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
            with cols[i]:
                st.markdown(f"### {m['home']}")
                st.write("vs")
                st.markdown(f"### {m['away']}")
                st.caption(f"⏰ {m['time']}")
                # 선택 버튼만 박스 하단에 배치
                if st.button("분석", key=f"sel_{idx}"):
                    st.session_state.target_home = m['home']
                    st.session_state.target_away = m['away']
                    st.rerun()

with c3:
    if st.button("▶️"): st.session_state.page += 1

# 4. 선택된 경기 표시
if 'target_home' not in st.session_state: 
    st.session_state.target_home = matches[0]['home']
    st.session_state.target_away = matches[0]['away']

st.divider()
st.subheader(f"선택 경기: {st.session_state.target_home} vs {st.session_state.target_away}")
