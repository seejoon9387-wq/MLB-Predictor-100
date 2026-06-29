# modules/feature_selector.py
import pandas as pd
import numpy as np

def remove_collinear_features(df, threshold=0.9):
    """
    상관관계가 높은 피처들을 제거하여 독립성 확보
    """
    corr_matrix = df.corr().abs()
    # 상삼각 행렬 추출
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    
    # 임계값 이상의 상관관계를 가지는 피처명 식별
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    
    df_reduced = df.drop(columns=to_drop)
    print(f"제거된 공선성 피처 수: {len(to_drop)}")
    return df_reduced
