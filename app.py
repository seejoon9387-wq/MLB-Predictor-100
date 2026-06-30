import sys
import os

# 1. 시스템 경로 자동 최적화
# 프로젝트 루트를 찾아 시스템 경로에 추가
base_path = os.path.dirname(os.path.abspath(__file__))
if base_path not in sys.path:
    sys.path.insert(0, base_path)

import streamlit as st

# 2. 유연한 모듈 로딩 (경로 문제 방지)
try:
    # engine.py가 루트에 있을 경우를 우선 시도
    from engine import SabermetricsEngine
except ImportError:
    try:
        # engine.py가 modules 폴더 안에 있을 경우를 대비
        from modules.engine import SabermetricsEngine
    except ImportError:
        st.error("❌ 'engine.py' 파일을 찾을 수 없습니다. 파일이 프로젝트 루트나 'modules/' 폴더에 있는지 확인하세요.")
        st.stop()

from modules.data_manager import DataManager

# 3. UI 설정
st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")
st.title("⚾ MLB 예측 분석 엔진")

# 4. 입력 UI
col1, col2, col3 = st.columns(3)
with col1: match_date = st.date_input("날짜 선택")
with col2: home_team = st.text_input("홈팀")
with col3: away_team = st.text_input("원정팀")

if st.button("분석 시작"):
    if not home_team or not away_team:
        st.error("팀 이름을 모두 입력해주세요.")
    else:
        try:
            st.write(f"⚙️ {home_team} vs {away_team} 분석 진행 중...")
            
            # 엔진 실행
            engine = SabermetricsEngine()
            mock_data = {
                'home': home_team, 'away': away_team,
                'lineup': ['Player1', 'Player2'],
                'pitcher_stamina': {'last_pitch_count': 90},
                'weather': {'temp_f': 75}
            }
            
            result = engine.execute(mock_data)
            
            st.success("분석 완료!")
            st.metric(label="승리 확률", value=f"{result.get('win_prob', 0)}%")
            
            with st.expander("분석 상세 확인"):
                st.json(result)
                
        except Exception as e:
            st.error(f"❌ 분석 중 오류 발생: {str(e)}")
