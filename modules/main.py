# [파일: main.py]
import pandas as pd
from config import SCHEMA
from engine import MatchAnalysisEngine

def run_match_briefing(match_data, historical_data, historical_target):
    # 1. 엔진 가동
    engine = MatchAnalysisEngine(SCHEMA)
    clean_hist = engine.clean(historical_data)
    engine.train(clean_hist, historical_target)
    
    # 2. 분석 브리핑 생성
    brief = engine.get_analysis_brief(match_data)
    
    # 3. 상세 브리핑 출력
    print("--- 📋 경기 예측 상세 브리핑 ---")
    print(f"예측 결과 값: {brief['predicted_score']:.2f}")
    print(f"예측 신뢰도: {brief['confidence']}")
    print("분석의 핵심 근거:")
    for factor, weight in brief['top_factors'].items():
        print(f"- {factor}: 영향력 {weight*100:.1f}%")
    print("------------------------------")

if __name__ == "__main__":
    # 과거 데이터 및 현재 경기 데이터 예시
    hist_data = pd.DataFrame({'feature1': [10, 50, 80], 'feature2': [0.1, 0.5, 0.9]})
    hist_target = [0, 1, 1]
    current_match = pd.DataFrame({'feature1': [75], 'feature2': [0.8]})
    
    run_match_briefing(current_match, hist_data, hist_target)
