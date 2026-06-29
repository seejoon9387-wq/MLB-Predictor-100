import streamlit as st
import pandas as pd
from modules.main_trainer import MLBUnifiedTrainer

def main():
    st.title("⚾ MLB AI 분석 대시보드")
    
    # 분석 데이터 (데이터 소스)
    data = {
        'h_era': 3.5, 'a_era': 4.2, 
        'h_ops': 0.85, 'a_ops': 0.78,
        'h_last_10': 0.7, 'a_last_10': 0.4,
        'h_avg': 0.27, 'a_avg': 0.25,
        'h_win_rate': 0.64, 'a_win_rate': 0.52
    }
    
    if st.button("🚀 유기적 통합 엔진 가동"):
        trainer = MLBUnifiedTrainer()
        result = trainer.analyze(data)
        
        st.metric("예측 승자", result['winner'])
        st.metric("확신도", f"{result['confidence']}%")
        
        st.markdown("### 📋 분석 근거 데이터")
        # 데이터가 있는 키만 동적으로 추출하여 오류 차단
        df = pd.DataFrame([
            {"지표": key.upper(), "Home": data.get(f"h_{key}"), "Away": data.get(f"a_{key}")}
            for key in ['win_rate', 'era', 'ops', 'avg', 'last_10']
        ])
        st.table(df)
        st.progress(result['score'])

if __name__ == "__main__":
    main()
