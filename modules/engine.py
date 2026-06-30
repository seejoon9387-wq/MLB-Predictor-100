import joblib
import os
import pandas as pd
from modules.data_loader import prepare_inference_features
from modules.matchup import get_team_matchup_adjustment
from modules.stamina_engine import get_stamina_adjustment
from modules.weather_engine import get_climate_adjustment
from modules.calibrator import calibrate_probability

class SabermetricsEngine:
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
        
        # 3. 보정 파이프라인 (상성 + 피로도 + 날씨)
        lineup_df = pd.DataFrame(data.get('lineup', []))
        adj = (get_team_matchup_adjustment(lineup_df) + 
               get_stamina_adjustment(data.get('pitcher_stamina', {})) + 
               get_climate_adjustment(data.get('weather', {})))
        
        # 4. 캘리브레이션 (통계적 교정)
        final_prob = calibrate_probability(raw_prob + adj)
        
        return {
            "win_prob": round(final_prob * 100, 2),
            "raw_prob": round(raw_prob * 100, 2),
            "adjustments": round(adj * 100, 2),
            "status": "success"
        }
