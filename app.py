import sys
import os

# 1. 경로 설정 (프로젝트 루트를 파이썬 모듈 탐색 경로 최상단에 추가)
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
# 경로 설정 후 import 수행
from engine import SabermetricsEngine
from modules.data_manager import DataManager

# 2. UI 설정
st.set_page_config(page_title="MLB 예측 분석 엔진", layout="wide")
st.title("⚾ MLB 예측 분석 엔진")
st.subheader("데이터 기반 승률 예측 및 브리핑 시스템")

# 3. 사용자 입력란
col1, col2, col3 = st.columns(3)
with col1:
    match_date = st.date_input("날짜 선택")
with col2:
    home_team = st.text_input("홈팀")
with col3:
    away_team = st.text_input("원정팀")

# 4. 분석 실행 버튼
if st.button("분석 시작"):
    if not home_team or not away_team:
        st.error("팀 이름을 모두 입력해주세요.")
    else:
        try:
            st.write(f"⚙️ {home_team} vs {away_team} 경기 데이터 호출 및 분석 중...")
            
            # 엔진 초기화
            engine = SabermetricsEngine()
            
            # 가상 데이터 구성 (실제 DB 연동 시 DataManager.get_game_data 호출로 대체 가능)
            mock_data = {
                'home': home_team, 
                'away': away_team,
                'lineup': ['Player1', 'Player2'], 
                'pitcher_stamina': {'last_pitch_count': 90, 'days_rest': 4},
                'weather': {'temp_f': 75, 'wind_speed': 5, 'wind_dir_deg': 180}
            }
            
            # 분석 결과 도출
            result = engine.execute(mock_data)
            
            # 5. 결과 시각화
            st.success("분석 완료!")
            
            # 승률 미터기
            st.metric(label=f"{home_team} 승리 확률", value=f"{result['win_prob']}%")
            
            # 상세 내용 브리핑
            with st.expander("상세 분석 데이터 확인"):
                st.write("조정 항목 상세:")
                st.json(result.get('adjustment_details', {}))
                st.write("전체 결과값:")
                st.json(result)
                
        except Exception as e:
            # 상세 에러 출력
            st.error(f"❌ 분석 중 오류가 발생했습니다.")
            st.write("오류 상세 내용:")
            st.code(f"{type(e).__name__}: {str(e)}")
            st.info("💡 팁: 'engine.py'나 모듈 파일 내부에 문법 오류가 없는지, 데이터 파일 경로가 올바른지 확인해주세요.")
