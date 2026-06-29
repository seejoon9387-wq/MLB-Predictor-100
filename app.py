import streamlit as st
import pandas as pd
from modules.main_trainer import MLBUnifiedTrainer

def main():
    st.title("⚾ MLB AI 전문 분석 대시보드")
    
    if st.button("🚀 유기적 통합 엔진 가동"):
        with st.spinner('40개 통계 모듈 동기화 및 분석 중...'):
            result = MLBUnifiedTrainer().analyze({})
            
            col1, col2 = st.columns(2)
            col1.metric("예측 승자", result['winner'])
            col2.metric("확신도", f"{result['confidence']}%")
            
            st.markdown("### 📋 분석 근거 데이터")
            stats = result['stats']
            # 키 이름을 h_rate, h_era 등으로 통일
            st.table(pd.DataFrame({
                "구분": ["시즌 승률", "방어율(ERA)"],
                "Home": [f"{int(stats['h_rate']*100)}%", stats['h_era']],
                "Away": [f"{int(stats['a_rate']*100)}%", stats['a_era']]
            }))
            
            st.markdown("---")
            st.write(result['detailed_report'])
            st.progress(result['score'])

if __name__ == "__main__":
    main()
