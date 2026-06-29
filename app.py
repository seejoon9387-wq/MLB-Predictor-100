import sys
import os
import streamlit as st
import pandas as pd
from modules.data_loader import load_data
from modules.main_trainer import MLBUnifiedTrainer

sys.path.append(os.getcwd())

st.set_page_config(page_title="MLB AI Intelligence Engine", layout="wide")

def main():
    st.title("⚾ MLB AI Intelligence Engine: 분석 대시보드")
    
    # 사이드바 설정
    st.sidebar.header("엔진 컨트롤")
    mode = st.sidebar.radio("분석 모드:", ("연속적", "독립적"))
    game_pk = st.sidebar.text_input("분석할 경기 ID (game_pk):", "718000")
    
    # 1. 데이터 로드 (상시 수행)
    try:
        registry = load_data(analysis_mode=(mode == "연속적"))
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
        return

    # 2. 메인 레이아웃 (버튼 클릭 전에도 표시)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 엔진 정밀 분석 브리핑")
        briefing_placeholder = st.empty() # 결과를 담을 빈 공간
        briefing_placeholder.info("왼쪽 사이드바에서 분석을 실행하세요.")
        
    with col2:
        st.subheader("📈 승률 확률 분포 (몬테카를로)")
        chart_placeholder = st.empty() # 차트를 담을 빈 공간
        chart_placeholder.line_chart(pd.DataFrame([0.5], columns=['Win_Prob']))

    # 3. 분석 실행 시 로직 업데이트
    if st.sidebar.button("데이터 분석 실행"):
        try:
            trainer = MLBUnifiedTrainer()
            briefing = trainer.get_briefing(int(game_pk))
            
            # 플레이스홀더를 결과물로 교체
            briefing_placeholder.info(briefing)
            chart_placeholder.line_chart(pd.DataFrame([0.1, 0.3, 0.6, 0.3, 0.1], columns=['Win_Prob']))
            
            st.divider()
            st.subheader("💰 전체 경기 수익성 순위")
            st.dataframe(registry.head(20), use_container_width=True)
            
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
