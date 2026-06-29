import sys
import os

# 1. 프로젝트 최상위 경로를 파이썬 경로에 강제 삽입 (절대 경로 방식)
# Streamlit Cloud의 루트 경로는 /mount/src/mlb-predictor-100/ 입니다.
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

import streamlit as st
import pandas as pd

# 2. 로깅을 통해 현재 경로 상태 확인 (디버깅용)
print(f"DEBUG: Current Working Directory: {os.getcwd()}")
print(f"DEBUG: Python Path: {sys.path}")

# 3. 모듈 임포트 시도
try:
    from modules.data_loader import load_data
    from main_trainer import MLBUnifiedTrainer
except ImportError as e:
    st.error(f"임포트 실패: {e}")
    st.write("현재 경로 내 파일 목록:", os.listdir(project_root))
    st.stop()

st.set_page_config(page_title="MLB AI Engine", layout="wide")

def main():
    st.title("⚾ MLB AI Intelligence Engine")
    
    # 분석 모드 및 경기 ID 입력
    mode = st.sidebar.radio("분석 모드:", ("연속적", "독립적"))
    game_pk = st.sidebar.text_input("경기 ID (예: 718000):", "718000")
    
    if st.sidebar.button("데이터 분석 실행"):
        try:
            # 데이터 로드 및 분석
            trainer = MLBUnifiedTrainer()
            briefing = trainer.get_briefing(int(game_pk))
            
            st.info(briefing)
        except Exception as e:
            st.error(f"분석 중 오류: {e}")

if __name__ == "__main__":
    main()
