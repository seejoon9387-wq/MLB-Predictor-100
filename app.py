import sys
import os

# 현재 app.py가 있는 폴더를 시스템 경로에 강제로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from engine import SabermetricsEngine  # 이제 이 코드가 작동할 것입니다.
from modules.data_manager import DataManager

import streamlit as st
from engine import SabermetricsEngine
from modules.data_manager import DataManager

# 1. UI 설정
st.title("MLB 예측 분석 엔진")
st.subheader("데이터 기반 승률 예측 및 브리핑")

# 2. 사용자 입력란
col1, col2, col3 = st.columns(3)
with col1:
    match_date = st.date_input("날짜 선택")
with col2:
    home_team = st.text_input("홈팀")
with col3:
    away_team = st.text_input("원정팀")

if st.button("분석 시작"):
    if not home_team or not away_team:
        st.error("팀 이름을 모두 입력해주세요.")
    else:
        try:
            # 3. 데이터 호출 및 분석 프로세스 시작
            st.write(f"⚙️ {home_team} vs {away_team} 경기 데이터 호출 중...")
            
            # 엔진 초기화
            engine = SabermetricsEngine()
            
            # 테스트용 가상 데이터 생성 (실제 DB 연동 시 DataManager 사용)
            # 여기를 DataManager.get_game_data(home_team, away_team) 등으로 연결
            mock_data = {
                'home': home_team, 'away': away_team,
                'lineup': ['Player1', 'Player2'], # 실제 명단 연동 가능
                'pitcher_stamina': {'last_pitch_count': 90, 'days_rest': 4},
                'weather': {'temp_f': 75, 'wind_speed': 5, 'wind_dir_deg': 180}
            }
            
            # 4. 분석 결과 도출
            result = engine.execute(mock_data)
            
            # 5. 결과 시각화
            st.success("분석 완료!")
            st.metric(label="승리 확률", value=f"{result['win_prob']}%")
            
            with st.expander("상세 데이터 및 조정값 확인"):
                st.json(result)
                
        except Exception as e:
            # 에러 발생 시 상세 정보 출력
            st.error(f"❌ 분석 중 에러가 발생했습니다.")
            st.code(str(e))
            st.info("데이터베이스에서 해당 경기 정보를 찾을 수 없거나 모듈 호출 과정에 오류가 있습니다.")
