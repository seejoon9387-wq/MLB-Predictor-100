import sys
import os
import streamlit as st

# 1. 시스템 경로 자동 탐색 및 등록
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 2. 유연한 모듈 임포트 로직
def load_modules():
    global SabermetricsEngine, DataManager
    try:
        # 1차 시도: 루트에서 찾기
        from engine import SabermetricsEngine
    except ImportError:
        # 2차 시도: modules 폴더에서 찾기
        try:
            from modules.engine import SabermetricsEngine
        except ImportError:
            st.error("❌ 'engine.py'를 찾을 수 없습니다. 파일이 루트나 'modules/' 폴더에 있는지 확인하세요.")
            st.stop()
            
    try:
        from modules.data_manager import DataManager
    except ImportError:
        st.error("❌ 'modules/data_manager.py'를 찾을 수 없습니다.")
        st.stop()

load_modules()

# 3. UI 구성
st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")
st.title("⚾ MLB 예측 분석 엔진")

# 사용자 입력
col1, col2, col3 = st.columns(3)
with col1: match_date = st.date_input("날짜 선택")
with col2: home_team = st.text_input("홈팀")
with col3: away_team = st.text_input("원정팀")

# 분석 버튼
if st.button("분석 시작"):
    if not home_team or not away_team:
        st.error("팀 이름을 모두 입력해주세요.")
    else:
        try:
            st.write(f"⚙️ {home_team} vs {away_team} 분석 가동 중...")
            
            # 엔진 실행
            engine = SabermetricsEngine()
            
            # 테스트 데이터 (실제 DB 데이터로 대체 예정)
            mock_data = {
                'home': home_team, 'away': away_team,
                'lineup': ['Player1', 'Player2'],
                'pitcher_stamina': {'last_pitch_count': 90},
                'weather': {'temp_f': 75}
            }
            
            result = engine.execute(mock_data)
            
            # 결과 출력
            st.success("분석 완료!")
            st.metric(label="승리 확률", value=f"{result.get('win_prob', 0)}%")
            
            with st.expander("분석 상세 확인"):
                st.json(result)
                
        except Exception as e:
            st.error(f"❌ 분석 중 오류 발생")
            st.code(f"오류 내용: {str(e)}")

# 4. 파일 구조 확인용 (디버깅용 - 문제 해결 후 삭제 가능)
with st.expander("파일 구조 디버깅"):
    st.write("현재 디렉토리 파일 목록:")
    st.write(os.listdir('.'))
    if os.path.exists('modules'):
        st.write("modules 폴더 내부 파일 목록:")
        st.write(os.listdir('modules'))
