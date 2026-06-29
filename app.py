import streamlit as st
from modules.main_trainer import MLBUnifiedTrainer
from modules.ui_manager import UIManager
from modules.registry import Registry

def main():
    st.set_page_config(page_title="MLB AI Analyst", layout="wide")
    
    # 1. 데이터 로드 및 엔진 구동
    # 실제 데이터는 registry를 통해 각 엔진 모듈에서 합산됨
    raw_data = {'h_era': 3.5, 'a_era': 4.2, 'h_ops': 0.85, 'a_ops': 0.78}
    trainer = MLBUnifiedTrainer()
    result = trainer.analyze(raw_data)
    
    # 2. UI 렌더링 (하드코딩된 더미 데이터 예시)
    games = [
        {'away_name': 'WSH', 'away_score': 6, 'home_name': 'BAL', 'home_score': 4},
        {'away_name': 'CIN', 'away_score': 4, 'home_name': 'PIT', 'home_score': 9},
    ]
    
    # 3. 전체 레이아웃 구성
    UIManager.render_game_navbar(games)
    st.divider()
    UIManager.render_main_dashboard(result)

if __name__ == "__main__":
    main()
