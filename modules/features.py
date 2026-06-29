import pandas as pd

def add_rolling_features(registry):
    """
    팀별 다중 윈도우 이동 평균(3, 5, 10, 30경기) 생성
    """
    registry = registry.sort_index()
    
    # 생성할 윈도우 사이즈 리스트
    windows = [3, 5, 10, 30]
    
    # 이동 평균을 계산할 타겟 지표들
    target_cols = ['launch_speed', 'woba_value']
    
    # 각 윈도우별로 이동 평균 컬럼 생성
    for window in windows:
        for col in target_cols:
            col_name = f'rolling_{col}_{window}g'
            # 팀별로 그룹화하여 이동 평균 산출
            registry[col_name] = registry.groupby('home_team')[col].transform(
                lambda x: x.rolling(window=window, min_periods=1).mean()
            )
            
    return registry
