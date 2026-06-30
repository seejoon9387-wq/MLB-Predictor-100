import joblib
import os
import pandas as pd
from modules.data_loader import prepare_inference_features
from modules.matchup import get_team_matchup_adjustment # 가정한 함수명

class BaseEngine:
    def execute(self, data):
        raise NotImplementedError("각 엔진은 execute 메서드를 구현해야 합니다.")

class SabermetricsEngine(BaseEngine):
    def __init__(self, model_path="models/mlb_model.pkl"):
        # 모델 로드 (추론용)
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {model_path}")

    def execute(self, data):
        """
        추론 및 보정 파이프라인 통합
        """
        # 1. 추론을 위한 피처 정제
        processed_data = prepare_inference_features(data)
        
        # 2. 모델 기반 추론 (Raw Probability)
        features_df = pd.DataFrame([processed_data])
        raw_prob = self.model.predict_proba(features_df)[0][1] # 홈팀 승리 확률
        
        # 3. 보정 로직 적용
        final_prob = self.apply_calibrations(raw_prob, processed_data)
        
        return {
            "win_prob": round(final_prob * 100, 2),
            "raw_prob": round(raw_prob * 100, 2),
            "adjustment": round((final_prob - raw_prob) * 100, 2),
            "status": "success"
        }

    def apply_calibrations(self, prob, data):
        """
        여러 모듈의 보정치를 순차적으로 적용하는 통합 함수
        """
        # 상성 보정치 산출 (matchup 모듈 활용)
        matchup_adj = get_team_matchup_adjustment(data.get('lineup', []), data.get('pitcher', ''))
        
        # 최종 확률 계산 (확률 범위를 0~1로 제한)
        final_prob = prob + matchup_adj
        return max(0.0, min(1.0, final_prob))
