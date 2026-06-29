import streamlit as st
from modules.main_trainer import MLBUnifiedTrainer
from modules.ui_manager import UIManager

def main():
    st.set_page_config(layout="wide")
    
    # 1. 데이터 가져오기 (API 연동 시 여기만 수정)
    data = {'h_era': 3.5, 'a_era': 4.2, 'h_ops': 0.85, 'a_ops': 0.78, 'h_win_rate': 0.64, 'a_win_rate': 0.52}
    
    # 2. 분석 엔진 구동
    trainer = MLBUnifiedTrainer()
    result = trainer.analyze(data)
    
    # 3. UI 렌더링 (UI가 바뀌어도 로직은 안전)
    UIManager.render_scoreboard("Orioles", 5, "White Sox", 3)
    
    col1, col2 = st.columns(2)
    col1.metric("예측 승자", result['winner'])
    col2.metric("확신도", f"{result['confidence']}%")
    
    UIManager.render_stats_table(result['stats'])

if __name__ == "__main__":
    main()
