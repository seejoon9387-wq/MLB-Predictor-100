import sys
import os
import streamlit as st
import pandas as pd
from modules.data_loader import load_data
from modules.main_trainer import MLBUnifiedTrainer

# 프로젝트 루트 경로 확보
sys.path.append(os.getcwd())

st.set_page_config(page_title="MLB AI Intelligence Engine", layout="wide")

def main():
    st.title("⚾ MLB AI Intelligence Engine: 분석 대시보드")
    
    # 1. 사이드바 설정
    st.sidebar.header("엔진 컨트롤")
    mode = st.sidebar.radio("데이터 분석 모드:", ("연속적", "독립적"))
    game_pk = st.sidebar.text_input("분석할 경기 ID (game_pk):", "718000")
    
    # 데이터 로드
    try:
        registry = load_data(analysis_mode=(mode == "연속적"))
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return

    # 2. 분석 실행 로직
    if st.sidebar.button("데이터 분석 실행"):
        try:
            trainer = MLBUnifiedTrainer()
            
            # (1) 상세 브리핑 출력
            briefing = trainer.get_briefing(int(game_pk))
            
            # 레이아웃 구성
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📊 엔진 정밀 분석 브리핑")
                st.info(briefing)
            
            with col2:
                st.subheader("📈 승률 확률 분포 (몬테카를로)")
                # 시뮬레이션 확률 분포 차트 (예시 데이터)
                chart_data = pd.DataFrame([0.1, 0.25, 0.6, 0.25, 0.1], columns=['Probability'])
                st.line_chart(chart_data)
            
            # (2) 전체 수익성 순위 테이블 출력
            st.divider()
            st.subheader("💰 전체 경기 수익성 순위 (Expected Value)")
            
            # 수익성 데이터 추출 (데이터프레임 내에 expected_value가 있다고 가정)
            if 'expected_value' in registry.columns:
                display_df = registry[['game_pk', 'expected_value']].sort_values(by='expected_value', ascending=False)
                st.dataframe(display_df.head(20), use_container_width=True)
            else:
                st.warning("수익성 데이터(expected_value)가 계산되지 않았습니다.")
                st.dataframe(registry.head(10), use_container_width=True)
                
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
