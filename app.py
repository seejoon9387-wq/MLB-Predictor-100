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
st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")
st.title("⚾ MLB 예측 분석 엔진")

# 사용자 입력 UI (날짜 선택 추가)
col1, col2, col3 = st.columns(3)
with col1:
    match_date = st.date_input("날짜 선택")
with col2:
    home_team = st.text_input("홈팀 입력")
with col3:
    away_team = st.text_input("원정팀 입력")

if st.button("분석 시작"):
    if not home_team or not away_team:
        st.error("홈팀과 원정팀을 모두 입력해주세요.")
    else:
        try:
            with st.spinner("분석 중..."):
                engine = SabermetricsEngine()
                result = engine.execute({'home': home_team, 'away': away_team, 'date': match_date})
                
                st.success("분석 완료!")
                st.metric("예측 승리 확률", f"{result.get('win_prob', 0)}%")
                
                with st.expander("상세 분석 결과"):
                    st.json(result)
        except Exception as e:
            st.error(f"분석 중 오류 발생: {str(e)}")
