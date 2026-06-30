import numpy as np

def calibrate_probability(prob):
    """
    모델이 낸 확률(prob)이 실제 승률 분포와 일치하도록 보정하는 함수
    (예: 모델이 과신하는 경향이 있다면 이를 완화)
    """
    # Isotonic Regression의 근사치를 Sigmoid 굴곡으로 적용
    # 이 로직은 백테스팅 데이터를 통해 얻은 계수로 주기적으로 업데이트합니다.
    a = 1.05 # 편향 계수
    b = -0.025 # 오프셋
    
    calibrated_prob = 1 / (1 + np.exp(-(a * np.log(prob / (1 - prob)) + b)))
    
    return max(0.01, min(0.99, calibrated_prob))
