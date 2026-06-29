import streamlit as st
from modules.main_trainer import MLBUnifiedTrainer
from modules.ui_manager import UIManager
from modules.registry import Registry # 통합 저장소 호출

def main():
    # 1. 데이터 파이프라인 호출 (50개 모듈의 결과 취합)
    raw_data = Registry.get_all_engine_results() 
    
    # 2. 엔진 가동
    trainer = MLBUnifiedTrainer()
    final_result = trainer.analyze(raw_data)
    
    # 3. UI 렌더링 (UI 코드를 직접 건드리지 않음)
    UIManager.display_dashboard(final_result)

if __name__ == "__main__":
    main()
