import sys
import os
import streamlit as st

# 1. 시스템 경로 설정
project_root = os.getcwd()
if project_root not in sys.path:
    sys.path.insert(0, project_root)

st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")
st.title("⚾ MLB 예측 분석 엔진")

# 2. 명시적으로 modules.engine에서 호출
try:
    from modules.engine import SabermetricsEngine
    from modules.data_manager import DataManager
    st.success("✅ 엔진 모듈 로드 성공!")
except ImportError as e:
    st.error(f"❌ 모듈 로드 실패: {e}")
    st.write("파일 목록을 다시 확인하세요.")
    st.stop()

# 3. 분석 UI
home_team = st.text_input("홈팀 입력")
away_team = st.text_input("원정팀 입력")

if st.button("분석 시작"):
    if home_team and away_team:
        try:
            engine = SabermetricsEngine()
            mock_data = {'home': home_team, 'away': away_team}
            
            # 분석 엔진 실행
            result = engine.execute(mock_data)
            
            st.success("분석 완료!")
            st.metric("예측 승리 확률", f"{result.get('win_prob', 0)}%")
            
            with st.expander("상세 분석 결과"):
                st.json(result)
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")
