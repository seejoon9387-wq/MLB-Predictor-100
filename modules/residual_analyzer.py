# modules/residual_analyzer.py
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_residuals(y_true, y_pred):
    """
    잔차를 계산하고 패턴을 시각화하여 모델의 체계적 오류 분석
    """
    residuals = y_true - y_pred
    
    # 1. 잔차 플롯 (Residual Plot)
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted Value')
    plt.ylabel('Residuals')
    plt.title('Residual Analysis: Patterns of Prediction Failure')
    plt.show()
    
    # 2. 잔차의 분포 확인 (정규성 검정)
    sns.histplot(residuals, kde=True)
    plt.title('Residual Distribution')
    plt.show()
    
    return residuals
