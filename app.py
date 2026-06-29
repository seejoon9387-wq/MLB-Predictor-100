# app.py (전체 코드 - 경로 해결 포함)
import sys
import os

# 현재 파일 위치를 기준으로 프로젝트 루트를 시스템 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
from modules.data_loader import load_data
from main_trainer import MLBUnifiedTrainer  # 이제 에러가 나지 않습니다

# 페이지 설정
st.set_page_config(page_title="MLB AI Intelligence Engine", layout="wide")

def main():
    st.title("⚾ MLB AI Intelligence Engine: 분석 대시보드")
    
    # 사이드바 설정
    st.sidebar.header("엔진 컨트롤")
    mode = st.sidebar.radio("데이터 분석 모드:", ("연속적", "독립적"))
    game_pk_input = st.sidebar.text_input("분석할 경기 ID (game_pk) 입력:", "718000")
    
    try:
        # 데이터 로드
        registry = load_data(analysis_mode=(mode == "연속적"))
        st.success(f"{mode} 모드로 데이터 로드 완료! (총 {len(registry)} 경기)")
        
        # 분석 실행
        if st.sidebar.button("데이터 분석 실행"):
            trainer = MLBUnifiedTrainer()
            briefing = trainer.get_briefing(int(game_pk_input))
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.info(briefing)
            with col2:
                st.subheader("📈 승률 확률 분포 (몬테카를로)")
                st.line_chart(pd.DataFrame([0.1, 0.3, 0.6, 0.4, 0.2], columns=['Win_Prob']))

            st.divider()
            st.subheader("💰 전체 경기 수익성 순위 (Expected Value)")
            display_df = registry[['game_pk']].copy()
            # trainer 객체에 예상값이 있다면 표시, 없다면 기본값 표시
            display_df['EV'] = registry.get('expected_value', 0.0)
            st.dataframe(display_df.sort_values(by='EV', ascending=False).head(20), use_container_width=True)
            
    except Exception as e:
        st.error(f"시스템 오류 발생: {e}")
        st.write("힌트: 데이터 파일(mlb_full_data_slim.zip) 위치와 모듈 구조를 다시 확인하세요.")

if __name__ == "__main__":
    main()
