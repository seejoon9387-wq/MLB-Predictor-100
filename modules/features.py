import pandas as pd

def add_rolling_features(registry):
    """
    팀별로 최근 3, 5, 10, 30경기 이동 평균을 생성하는 전체 코드
    (pandas 2.0+ 호환 버전)
    """
    # 1. 경기 날짜 순으로 정렬
    # 'game_date'가 없는 경우를 대비해 인덱스 정렬을 우선 시도
    if 'game_date' in registry.columns:
        registry = registry.sort_values(by=['game_date'])
    else:
        registry = registry.sort_index()
    
    # 2. 윈도우 사이즈와 대상 지표 정의
    windows = [3, 5, 10, 30]
    target_cols = ['launch_speed', 'woba_value']
    
    # 3. 각 윈도우별 이동 평균 생성 루프
    for window in windows:
        for col in target_cols:
            if col in registry.columns:
                col_name = f'rolling_{col}_{window}g'
                # 팀별 그룹화 후 이동 평균 계산
                registry[col_name] = registry.groupby('home_team')[col].transform(
                    lambda x: x.rolling(window=window, min_periods=1).mean()
                )
    
    # 4. 결측치 처리 (최신 pandas 문법 사용)
    # bfill(): 뒷방향(미래) 값으로 앞쪽 결측치를 채움
    registry = registry.bfill()
    
    return registry
