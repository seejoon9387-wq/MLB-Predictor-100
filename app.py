import streamlit as st
import pandas as pd
from modules.data_loader import load_data
from main_trainer import MLBUnifiedTrainer

# 페이지 설정
st.set_page_config(page_title="MLB AI Intelligence Engine", layout="wide")

def main():
    st.title("⚾ MLB AI Intelligence Engine: 분석 대시보드")
    
    # 1. 사이드바: 엔진 제어
    st.sidebar.header("엔진 컨트롤")
    mode = st.sidebar.radio("데이터 분석 모드:", ("연속적", "독립적"))
    game_pk_input = st.sidebar.text_input("분석할 경기 ID (game_pk) 입력:", "718000")
    
    # 데이터 로드 및 분석 엔진 초기화
    try:
        trainer = MLBUnifiedTrainer() # main_trainer의 클래스 호출
        registry = load_data(analysis_mode=(mode == "연속적"))
        
        st.success(f"{mode} 모드로 데이터 로드 완료! (총 {len(registry)} 경기)")
        
        # 2. 메인 화면: 선택된 경기에 대한 상세 브리핑
        st.subheader(f"📊 상세 분석 브리핑: Game {game_pk_input}")
        
        if st.sidebar.button("데이터 분석 실행"):
            # 브리핑 생성
            briefing = trainer.get_briefing(int(game_pk_input))
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.info(briefing)
                
            with col2:
                st.subheader("📈 승률 확률 분포 (몬테카를로)")
                # 시뮬레이션 확률 분포 시각화 (더미 데이터 예시)
                chart_data = pd.DataFrame([0.1, 0.3, 0.6, 0.4, 0.2], columns=['Win_Prob'])
                st.line_chart(chart_data)

            # 3. 전체 수익성 테이블
            st.divider()
            st.subheader("💰 전체 경기 수익성 순위 (Expected Value)")
            # 기대 수익 순으로 정렬
            display_df = registry[['game_pk', 'bayesian_win_rate']].copy()
            display_df['EV'] = registry.get('expected_value', 0)
            
            st.dataframe(display_df.sort_values(by='EV', ascending=False).head(20), use_container_width=True)
            
    except Exception as e:
        st.error(f"시스템 오류 발생: {e}")
        st.write("힌트: 데이터 파일(mlb_full_data_slim.zip)이 올바른 위치에 있는지 확인하세요.")

if __name__ == "__main__":
    main()
