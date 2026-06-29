import pandas as pd
import numpy as np

def remove_outliers(df, threshold=3):
    """
    Z-Score 기반 이상치 탐지:
    - 각 컬럼의 평균에서 3표준편차를 벗어나는 데이터를 이상치로 간주하여 제거
    - 수치형 컬럼에만 적용
    """
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # 평균과 표준편차 계산
            mean = df[col].mean()
            std = df[col].std()
            
            # 표준편차가 0이면 이상치가 없다고 판단
            if std == 0:
                continue
                
            # Z-Score 계산
            z_scores = (df[col] - mean) / std
            
            # |Z-Score| > 3 인 경우를 이상치로 간주하고 제거
            df = df[abs(z_scores) <= threshold]
            
    return df
