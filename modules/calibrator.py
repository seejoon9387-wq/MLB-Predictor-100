# modules/calibrator.py
from sklearn.calibration import CalibratedClassifierCV

def apply_probability_calibration(model, X_val, y_val):
    """
    등장 확률 교정 (Isotonic 또는 Sigmoid 방식 활용)
    """
    # 'isotonic'은 데이터가 많을 때, 'sigmoid'는 데이터가 적을 때 효과적
    calibrated_clf = CalibratedClassifierCV(
        estimator=model, 
        method='isotonic', 
        cv='prefit'
    )
    calibrated_clf.fit(X_val, y_val)
    return calibrated_clf
