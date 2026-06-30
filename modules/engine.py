import joblib
import os
from modules.data_loader import prepare_inference_features

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
        추론 및 보정 파이프라인
        """
        # 1. 추론을 위한 피처 정제
        processed_data = prepare_inference_features(data)
        
        # 2. 모델 기반 추론 (Raw Probability)
        # DataFrame 형태로 변환하여 모델에 입력
        features_df = pd.DataFrame([processed_data])
        raw_prob = self.model.predict_proba(features_df)[0][1] # 홈팀 승리 확률
        
        # 3. 보정 로직 적용 (BAYESIAN + MARKET)
        # 예: raw_prob에 베이지안 업데이트 등 가중치 적용
        final_prob = self.apply_calibrations(raw_prob, processed_data)
        
        return {
            "win_prob": round(final_prob * 100, 2),
            "raw_prob": round(raw_prob * 100, 2),
            "status": "success"
        }

    def apply_calibrations(self, prob, data):
        # 캘리브레이션 및 외부 보정 로직 (예: bayesian_win_rate 반영)
        bayesian_factor = data.get('bayesian_win_rate', 0)
        # 여기서 두 확률을 결합하는 로직을 고도화할 예정입니다.
        return (prob * 0.7) + (bayesian_factor * 0.3)
