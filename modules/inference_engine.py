import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import VotingClassifier

class InferenceEngine:
    def __init__(self):
        # 앙상블을 위한 기본 모델 설정
        self.model = self._build_ensemble_model()
        self.is_fitted = False

    def _build_ensemble_model(self):
        """GBM 기반 앙상블 모델 생성"""
        # 5단계: 앙상블(GBM) 및 확률 교정 적용
        base_model = XGBClassifier(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=6,
            use_label_encoder=False,
            eval_metric='logloss'
        )
        # 확률 보정(Calibration)을 통한 신뢰도 확보
        return CalibratedClassifierCV(base_model, method='sigmoid', cv=3)

    def fit(self, features):
        """데이터를 받아 모델 학습 수행"""
        # 31~40단계: 학습 모델링
        # features에는 'target' 컬럼이 포함되어 있다고 가정
        X = features.drop(columns=['target', 'game_id'], errors='ignore')
        y = features['target']
        
        print("[System] 모델 학습 수행 중...")
        self.model.fit(X, y)
        self.is_fitted = True
        return self.model

    def run_inference(self, features):
        """새로운 경기 데이터에 대한 예측 및 확률 반환"""
        if not self.is_fitted:
            raise ValueError("모델이 아직 학습되지 않았습니다.")
            
        X = features.drop(columns=['target', 'game_id'], errors='ignore')
        probs = self.model.predict_proba(X)
        
        # 승리 확률 반환
        return probs[:, 1]

    def get_feature_importance(self):
        """8단계: SHAP 기반 의사결정 시각화 근거 마련을 위한 기능"""
        # 향후 SHAP 연동 시 사용
        return "Feature Importance Map"
