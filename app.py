import streamlit as st
import sys
import subprocess

# 1. 필수 라이브러리 자동 설치 (환경 문제 자동 해결)
def install_requirements():
    required = ['pybaseball', 'pandas']
    for package in required:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_requirements()

# 2. 라이브러리 로드
import pandas as pd
from datetime import datetime
from pybaseball import schedule
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

# 3. 데이터 로드 (1시간 단위 캐싱으로 속도 최적화)
@st.cache_data(ttl=3600)
def get_live_schedule():
    year = datetime.now().year
    # MLB 시즌 전체 스케줄 로드
    df = schedule(year)
    # 필요한 컬럼만 추출
    return df[['Date', 'Away', 'Home']]

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
    with st.spinner('MLB 공식 서버에서 데이터를 가져오는 중...'):
        try:
            df = get_live_schedule()
            st.subheader("📅 경기 일정")
            
            # 테이블 클릭 이벤트 설정
            event = st.dataframe(
                df, 
                use_container_width=True,
                selection_mode="single-row",
                on_select="rerun"
            )
            
            # 4. 경기 선택 시 분석 실행
            if event.selection.rows:
                idx = event.selection.rows[0]
                selected_game = df.iloc[idx]
                
                st.divider()
                st.write(f"### 🔍 분석 대상: {selected_game['Away']} vs {selected_game['Home']} ({selected_game['Date']})")
                
                if st.button("🚀 엔진 가동 (분석 시작)"):
                    try:
                        # 모듈 내 Trainer 호출
                        trainer = MLBUnifiedTrainer()
                        # 분석 실행 (메서드 명은 실제 main_trainer.py와 일치해야 합니다)
                        st.info("엔진이 데이터를 분석 중입니다...")
                        # briefing = trainer.get_briefing(selected_game) # 필요 시 활성화
                    except Exception as e:
                        st.error(f"분석 중 오류 발생: {e}")
                        
        except Exception as e:
            st.error(f"데이터 로드 오류: {e}")

if __name__ == "__main__":
    main()
