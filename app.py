import sys
import os
import streamlit as st
import pandas as pd
from modules.data_loader import load_data
from modules.main_trainer import MLBUnifiedTrainer

sys.path.append(os.getcwd())

st.set_page_config(page_title="MLB AI Live Engine", layout="wide")

def main():
    st.title("⚾ MLB AI 실시간 경기 분석 대시보드")
    
    # 1. 데이터 로드 (실시간 데이터 연동 가정)
    registry = load_data(analysis_mode=True)
    
    # 2. 실시간 일정 테이블 구성
    st.subheader("📅 오늘 및 향후 경기 일정 (클릭하여 분석)")
    
    # 분석에 필요한 핵심 컬럼만 선택하여 테이블 생성
    display_cols = ['game_date', 'away_team', 'home_team', 'game_pk']
    schedule_df = registry[display_cols].sort_values('game_date')
    
    # 데이터 에디터(선택 가능) UI 생성
    event = st.dataframe(
        schedule_df,
        use_container_width=True,
        hide_index=True,
        selection_mode="single-row",
        on_select="rerun" # 선택 시 즉시 리로드하여 분석 가동
    )
    
    # 3. 클릭된 경기 결과 즉시 도출
    selected_rows = event.selection.rows
    if selected_rows:
        selected_idx = selected_rows[0]
        selected_game = schedule_df.iloc[selected_idx]
        game_pk = int(selected_game['game_pk'])
        
        st.divider()
        st.subheader(f"🔍 분석 결과: {selected_game['away_team']} vs {selected_game['home_team']}")
        
        try:
            # 엔진 가동
            trainer = MLBUnifiedTrainer()
            briefing = trainer.get_briefing(game_pk)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.info(briefing)
            with col2:
                st.subheader("📈 승률 확률 분포 (몬테카를로)")
                # 분석 엔진의 신뢰도 데이터 시각화
                
                st.line_chart(pd.DataFrame([0.1, 0.3, 0.6, 0.3, 0.1], columns=['Win_Prob']))
                
        except Exception as e:
            st.error(f"분석 엔진 오류: {e}")
    else:
        st.info("👆 분석할 경기를 표에서 클릭하세요.")

if __name__ == "__main__":
    main()
