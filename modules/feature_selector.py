import pandas as pd
import numpy as np

def select_optimal_features(df, threshold=0.9):
    """
    1. 다중공선성 제거 (독립성 확보)
    2. 예측력 없는 피처 식별 (상관관계 하위권 제거)
    """
    # 1. 상관관계 기반 공선성 제거
    corr_matrix = df.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    
    df_reduced = df.drop(columns=to_drop)
    
    # 2. 타겟 변수(예: home_win)와 상관관계가 너무 낮은 피처 제거 (예: 0.05 미만)
    # target 컬럼이 존재할 경우만 실행
    if 'home_win' in df_reduced.columns:
        target_corr = df_reduced.corr()['home_win'].abs()
        low_impact_features = target_corr[target_corr < 0.05].index.tolist()
        df_reduced = df_reduced.drop(columns=low_impact_features)
        
    print(f"제거된 공선성 피처: {len(to_drop)}개, 제거된 저영향 피처: {len(low_impact_features)}개")
    return df_reduced
