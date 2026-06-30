import joblib
import os
import pandas as pd
from modules.data_loader import prepare_inference_features
from modules.matchup import get_team_matchup_adjustment

class BaseEngine:
    def execute(self, data):
        raise NotImplementedError("각 엔진은 execute 메서드를 구현해야 합니다.")

class SabermetricsEngine(BaseEngine):
    def __init__(self, model_path="models/mlb_model.pkl"):
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {model_path}")

    def execute(self, data):
        # 1. 데이터 정제
        processed_data = prepare_inference_features(data)
        
        # 2. 모델 추론 (Raw)
        features_df = pd.DataFrame([processed_data])
        raw_prob = self.model.predict_proba(features_df)[0][1]
        
        # 3. 보정 적용
        # data['lineup']은 타자들의 정보가 담긴 데이터프레임 형태라고 가정합니다.
        lineup_df = pd.DataFrame(data.get('lineup', []))
        matchup_adj = get_team_matchup_adjustment(lineup_df)
        
        final_prob = raw_prob + matchup_adj
        final_prob = max(0.0, min(1.0, final_prob))
        
        return {
            "win_prob": round(final_prob * 100, 2),
            "raw_prob": round(raw_prob * 100, 2),
            "adjustment": round(matchup_adj * 100, 2),
            "status": "success"
        }
