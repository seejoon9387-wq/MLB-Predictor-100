import sys
import os

# 1. 절대 경로 강제 설정 (프로젝트 루트가 어디든 모듈을 찾게 함)
sys.path.append(os.getcwd())

import streamlit as st
import pandas as pd

# 2. 예외 처리된 임포트 (파일 구조에 따라 유연하게 대응)
try:
    from modules.data_loader import load_data
    from main_trainer import MLBUnifiedTrainer
except ImportError as e:
    st.error(f"모듈 임포트 실패: {e}")
    st.write("파일 구조를 확인하세요: main_trainer.py와 modules/ 폴더가 루트에 있어야 합니다.")
    st.stop()

st.set_page_config(page_title="MLB AI Engine", layout="wide")

def main():
    st.title("⚾ MLB AI Intelligence Engine: 분석 대시보드")
    
    # 사이드바
    mode = st.sidebar.radio("분석 모드:", ("연속적", "독립적"))
    game_pk = st.sidebar.text_input("경기 ID:", "718000")
    
    if st.sidebar.button("데이터 분석 실행"):
        try:
            # 엔진 초기화
            trainer = MLBUnifiedTrainer()
            
            # 분석 및 결과 출력
            briefing = trainer.get_briefing(int(game_pk))
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("분석 브리핑")
                st.info(briefing)
            with col2:
                st.subheader("예측 신뢰도")
                st.line_chart(pd.DataFrame([0.2, 0.4, 0.6, 0.8, 0.9]))
                
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
