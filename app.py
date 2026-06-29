import streamlit as st
import pandas as pd
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB AI Analyst Pro", layout="wide")

def main():
    st.title("⚾ MLB AI 전문 분석 대시보드")
    
    if st.button("🚀 엔진 가동"):
        with st.spinner('AI 분석 엔진 가동 중...'):
            try:
                # 1. 엔진이 요구하는 모든 필드를 명시적으로 포함
                # KeyError를 피하기 위해 필수 키(game_pk 등)를 모두 넣습니다.
                full_data_input = {
                    'game_pk': 824822,  # 예시 게임 PK
                    'bayesian_win_rate': 0.52,
                    'climate_adjusted_prob': 0.15,
                    'inefficiency_score': 0.08
                }
                
                # 2. 엔진 인스턴스 생성 및 데이터 전달
                trainer = MLBUnifiedTrainer()
                analysis_result = trainer.analyze(full_data_input)
                
                # 3. 결과 출력
                st.success("데이터 분석 완료")
                st.write("### 📊 분석 결과")
                st.json(analysis_result)
                
            except Exception as e:
                st.error(f"분석 오류: {e}")
                st.info("여전히 에러가 난다면, modules/main_trainer.py 내부에서 어떤 키를 호출하는지 확인이 필요합니다.")

if __name__ == "__main__":
    main()
