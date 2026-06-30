import joblib
import os
import pandas as pd
from modules.data_loader import prepare_inference_features
from modules.orchestrator import DataOrchestrator # 추가
from modules.calibrator import calibrate_probability

class SabermetricsEngine:
    def __init__(self, model_path="models/mlb_model.pkl"):
        self.model = joblib.load(model_path)
        self.orchestrator = DataOrchestrator() # 관리자 탑재

    def execute(self, data):
        # 1. 모델용 데이터 정제
        processed_data = prepare_inference_features(data)
        features_df = pd.DataFrame([processed_data])
        raw_prob = self.model.predict_proba(features_df)[0][1]
        
        # 2. 모든 보정치를 Orchestrator에게 일임
        adj_data = self.orchestrator.collect_all_data(data)
        total_adj = sum(adj_data.values())
        
        # 3. 캘리브레이션
        final_prob = calibrate_probability(raw_prob + total_adj)
        
        return {
            "win_prob": round(final_prob * 100, 2),
            "raw_prob": round(raw_prob * 100, 2),
            "adjustment_details": adj_data,
            "status": "success"
        }
