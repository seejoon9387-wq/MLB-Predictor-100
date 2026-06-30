# [파일: main.py]
import pandas as pd
from config import SCHEMA
from engine import MatchAnalysisEngine

def run_match_briefing(match_data, historical_data, historical_target):
    engine = MatchAnalysisEngine(SCHEMA)
    clean_hist = engine.clean(historical_data)
    engine.train(clean_hist, historical_target)
    
    brief = engine.get_analysis_brief(match_data)
    
    print("--- 📋 최종 경기 예측 상세 브리핑 ---")
    print(f"예측 결과 값: {brief['predicted_score']:.2f} ({brief['confidence']})")
    print(f"참고: 과거 인덱스 {brief['similar_match_idx']}번 경기 패턴과 유사함.")
    print("분석 결과 시각화가 완료되었습니다. (report_날짜.png 참조)")
    print("분석 이력이 analysis_log.txt에 기록되었습니다.")
    print("------------------------------------")

if __name__ == "__main__":
    hist_data = pd.DataFrame({'feature1': [10, 50, 80], 'feature2': [0.1, 0.5, 0.9]})
    hist_target = [0, 1, 1]
    current_match = pd.DataFrame({'feature1': [75], 'feature2': [0.8]})
    
    run_match_briefing(current_match, hist_data, hist_target)
