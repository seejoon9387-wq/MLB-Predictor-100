from sklearn.calibration import CalibratedClassifierCV
import xgboost as xgb

class ProbabilityCalibrator:
    def __init__(self, base_model):
        # 'isotonic' 또는 'sigmoid' 방식을 통한 확률 보정
        self.calibrated_model = CalibratedClassifierCV(
            estimator=base_model, 
            method='isotonic', 
            cv='prefit'
        )

    def fit_calibration(self, X_val, y_val):
        """검증 데이터를 사용하여 확률 보정 수행"""
        self.calibrated_model.fit(X_val, y_val)
        print("확률 캘리브레이션 완료.")

    def get_calibrated_prob(self, X):
        """보정된 확률값 반환"""
        return self.calibrated_model.predict_proba(X)

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    # Base 모델 가정 (분류기여야 함)
    base_model = xgb.XGBClassifier().fit([[0.1], [0.5], [0.9]], [0, 1, 1])
    
    calibrator = ProbabilityCalibrator(base_model)
    # 실제 환경에서는 보정용 데이터셋(X_val, y_val)을 입력
    print("캘리브레이션 모듈 준비 완료.")
