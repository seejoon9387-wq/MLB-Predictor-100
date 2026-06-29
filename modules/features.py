import pandas as pd

def add_rolling_features(registry):
    """
    최근 10경기 이동 평균 지표 생성
    """
    # 경기 순서대로 정렬 확인
    registry = registry.sort_index()
    
    # 윈도우 사이즈 (10경기)
    window = 10
    
    # 팀별로 묶어서 이동 평균 계산
    # 'home_team' 기준 그룹화하여 이동 평균 산출
    if 'home_team' in registry.columns and 'home_score' in registry.columns:
        registry['rolling_launch_speed'] = registry.groupby('home_team')['launch_speed'].transform(
            lambda x: x.rolling(window=window, min_periods=1).mean()
        )
        registry['rolling_score'] = registry.groupby('home_team')['home_score'].transform(
            lambda x: x.rolling(window=window, min_periods=1).mean()
        )
    
    return registry
