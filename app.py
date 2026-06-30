import sys
import os
import streamlit as st

# 1. 환경 설정 및 경로 강제 추가
project_root = os.getcwd()
if project_root not in sys.path:
    sys.path.insert(0, project_root)

st.set_page_config(page_title="MLB 엔진 디버거", layout="wide")
st.title("⚾ MLB 시스템 상태 확인")

# 2. 파일 부재 시 상세 원인 파악을 위한 디버그 로직
def debug_environment():
    files = os.listdir('.')
    st.write("### 현재 루트 디렉토리 파일 목록")
    st.write(files)
    
    if os.path.exists('modules'):
        st.write("### 'modules' 폴더 내부 파일 목록")
        st.write(os.listdir('modules'))
    else:
        st.error("❌ 'modules' 폴더를 찾을 수 없습니다.")

# 3. 모듈 강제 로드 시도
try:
    # 1. engine.py가 루트에 있을 경우
    from engine import SabermetricsEngine
    st.success("✅ 'engine.py'를 루트에서 찾았습니다!")
except ImportError:
    try:
        # 2. engine.py가 modules에 있을 경우
        from modules.engine import SabermetricsEngine
        st.success("✅ 'modules/engine.py'를 찾았습니다!")
    except ImportError:
        st.error("🚨 치명적 오류: 'engine.py' 파일을 찾을 수 없습니다.")
        debug_environment()
        st.stop()

# 4. 분석 UI (엔진 로드 성공 시에만 노출)
st.write("엔진이 정상적으로 로드되었습니다. 분석을 시작하세요.")

home_team = st.text_input("홈팀 입력")
away_team = st.text_input("원정팀 입력")

if st.button("분석 시작"):
    if home_team and away_team:
        try:
            engine = SabermetricsEngine()
            mock_data = {'home': home_team, 'away': away_team}
            result = engine.execute(mock_data)
            st.metric("승리 확률", f"{result.get('win_prob', 0)}%")
        except Exception as e:
            st.error(f"분석 중 오류: {e}")
