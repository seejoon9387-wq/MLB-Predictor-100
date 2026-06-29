import streamlit as st
import pandas as pd
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB AI Analyst", layout="wide")

def main():
    st.title("⚾ MLB AI 전문 분석 대시보드")
    
    # 분석 가동 버튼
    if st.button("🚀 엔진 가동 (데이터 기반 분석)"):
        with st.spinner('AI 분석 엔진이 데이터를 정밀 추론 중...'):
            try:
                # 1. 시뮬레이션용 데이터셋 (엔진이 요구하는 키 값 포함)
                data_input = {
                    'bayesian_win_rate': 0.52,
                    'climate_adjusted_prob': 0.15,
                    'inefficiency_score': 0.08
                }
                
                # 2. 엔진 인스턴스 생성 및 분석
                trainer = MLBUnifiedTrainer()
                analysis_result = trainer.analyze(data_input)
                
                # 3. 결과 출력
                st.success("데이터 분석 완료")
                st.write("### 📊 분석 결과 리포트")
                st.json(analysis_result)
                
            except Exception as e:
                st.error(f"엔진 분석 오류: {e}")
                st.info("simulator.py의 18행을 .get() 메서드로 수정했는지 확인해주세요.")

if __name__ == "__main__":
    main()
