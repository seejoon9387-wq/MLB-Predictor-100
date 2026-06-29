import pandas as pd
import numpy as np

def add_schedule_features(registry):
    """
    데이터 존재 여부를 확인하고, 안전하게 요일/시간/거리 피처를 생성합니다.
    """
    # 1. 날짜 및 요일 처리
    if 'game_date' in registry.columns:
        registry['game_date'] = pd.to_datetime(registry['game_date'], errors='coerce')
        registry['day_of_week'] = registry['game_date'].dt.dayofweek
        registry['is_weekend'] = registry['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    # 2. 시간 데이터 존재 확인 및 야간 경기 여부 처리
    # 컬럼명이 다를 경우를 대비하여 우선순위 후보군 확인
    time_col = next((c for c in ['game_time', 'start_time', 'time'] if c in registry.columns), None)
    
    if time_col:
        registry['is_night_game'] = registry[time_col].astype(str).apply(
            lambda x: 1 if ':' in x and int(x.split(':')[0]) >= 18 else 0
        )
    else:
        # 데이터가 없으면 기본값 0 할당
        registry['is_night_game'] = 0
    
    # 3. 이동 거리 초기화
    registry['travel_distance'] = 0.0
    
    return registry
