import streamlit as st
import pandas as pd
from modules.main_trainer import MLBUnifiedTrainer

def main():
    st.title("⚾ MLB AI 전문 분석 대시보드")
    
    if st.button("🚀 엔진 가동"):
        with st.spinner('분석 중...'):
            try:
                # 1. 데이터 준비 (딕셔너리 형태)
                data_input = {
                    'bayesian_win_rate': 0.52,
                    'climate_adjusted_prob': 0.15,
                    'inefficiency_score': 0.08
                }
                
                # 2. 엔진 분석
                trainer = MLBUnifiedTrainer()
                result = trainer.analyze(data_input)
                
                # 3. 결과 출력
                st.success("데이터 분석 완료")
                st.write("### 📊 분석 결과")
                st.write(result)
                
            except Exception as e:
                st.error(f"분석 오류: {e}")

if __name__ == "__main__":
    main()
