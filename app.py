import sys
import os

# 프로젝트 루트 경로 확보
sys.path.append(os.getcwd())

import streamlit as st
import pandas as pd

# 1. 파일 구조에 맞게 임포트 경로 수정
try:
    from modules.data_loader import load_data
    from modules.main_trainer import MLBUnifiedTrainer # modules 하위로 이동된 경로 반영
except ImportError as e:
    st.error(f"모듈 임포트 실패: {e}")
    st.write("파일 구조 확인: modules 폴더 안에 main_trainer.py가 있어야 합니다.")
    st.stop()

st.set_page_config(page_title="MLB AI Engine", layout="wide")

def main():
    st.title("⚾ MLB AI Intelligence Engine: 분석 대시보드")
    
    mode = st.sidebar.radio("분석 모드:", ("연속적", "독립적"))
    game_pk = st.sidebar.text_input("경기 ID:", "718000")
    
    if st.sidebar.button("데이터 분석 실행"):
        try:
            # 클래스 인스턴스화
            trainer = MLBUnifiedTrainer()
            # 브리핑 가져오기
            briefing = trainer.get_briefing(int(game_pk))
            
            st.info(briefing)
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
