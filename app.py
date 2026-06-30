import importlib
import modules.config
importlib.reload(modules.config) # 캐시 강제 삭제

import sys
import os
import streamlit as st

# 시스템 경로 설정
project_root = os.getcwd()
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 모듈 로드
try:
    from modules.engine import SabermetricsEngine
    from modules.data_manager import DataManager
    st.success("✅ 시스템 모듈 로드 완료")
except Exception as e:
    st.error(f"❌ 모듈 로드 실패: {e}")
    st.stop()

# UI 구성
st.title("⚾ MLB 예측 분석 엔진")
home_team = st.text_input("홈팀 입력")
away_team = st.text_input("원정팀 입력")

if st.button("분석 시작"):
    try:
        engine = SabermetricsEngine()
        result = engine.execute({'home': home_team, 'away': away_team})
        st.metric("예측 승리 확률", f"{result.get('win_prob', 0)}%")
    except Exception as e:
        st.error(f"분석 중 오류: {e}")
