import streamlit as st
import pandas as pd
from modules.main_trainer import MLBUnifiedTrainer

def main():
    st.title("⚾ MLB AI 전문 분석 대시보드")
    
    # 1. 일정표 (세션 상태에 저장하여 유지)
    st.subheader("📅 오늘의 경기 일정")
    df = pd.DataFrame([{'Time': '22:35', 'Away': 'Chicago White Sox', 'Home': 'Baltimore Orioles'}])
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 2. 분석 영역
    st.divider()
    if st.button("🚀 유기적 통합 엔진 가동"):
        with st.spinner('통계 데이터를 분석 중...'):
            result = MLBUnifiedTrainer().analyze({})
            
            col1, col2 = st.columns(2)
            col1.metric("예측 승자", result['winner'])
            col2.metric("확신도", f"{result['confidence']}%")
            
            st.markdown("### 📋 분석 근거 데이터")
            stats = result['stats']
            st.table(pd.DataFrame({
                "구분": ["시즌 승률", "방어율(ERA)"],
                "Home": [f"{int(stats['h_rate']*100)}%", stats['h_era']],
                "Away": [f"{int(stats['a_rate']*100)}%", stats['a_era']]
            }))
            st.write(result['detailed_report'])

if __name__ == "__main__":
    main()
