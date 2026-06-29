import pandas as pd

def calculate_z_score(df, column_name):
    """
    특정 컬럼에 대해 리그 평균 대비 Z-Score를 계산합니다.
    """
    mean = df[column_name].mean()
    std = df[column_name].std()
    
    # 표준편차가 0인 경우(모두 같은 값일 때) 대비 예외 처리
    if std == 0:
        return 0
        
    z_score = (df[column_name] - mean) / std
    return z_score

def add_z_score_features(registry):
    """
    주요 지표(woba, launch_speed 등)에 대해 Z-Score 피처 생성
    """
    target_metrics = ['woba_value', 'launch_speed']
    
    for metric in target_metrics:
        if metric in registry.columns:
            registry[f'{metric}_zscore'] = calculate_z_score(registry, metric)
            
    return registry
