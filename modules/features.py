import pandas as pd

def add_rolling_features(registry):
    """
    팀별로 최근 3, 5, 10, 30경기 이동 평균을 생성하는 전체 코드
    """
    # 1. 경기 날짜 순으로 정렬 (시계열 데이터 필수)
    registry = registry.sort_values(by=['game_date'])
    
    # 2. 윈도우 사이즈와 대상 지표 정의
    windows = [3, 5, 10, 30]
    target_cols = ['launch_speed', 'woba_value']
    
    # 3. 각 윈도우별 이동 평균 생성 루프
    for window in windows:
        for col in target_cols:
            if col in registry.columns:
                # 'home_team'을 기준으로 그룹화하여 순차적으로 이동 평균 계산
                col_name = f'rolling_{col}_{window}g'
                registry[col_name] = registry.groupby('home_team')[col].transform(
                    lambda x: x.rolling(window=window, min_periods=1).mean()
                )
    
    # 4. 결측치 처리 (첫 경기 등 데이터가 부족한 경우)
    registry = registry.fillna(method='bfill')
    
    return registry
