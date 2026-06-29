import pandas as pd
import numpy as np
from datetime import datetime

# 간단한 위도/경도 기반 거리 계산 (지구 곡률 고려)
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371 # 지구 반경(km)
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

def add_schedule_features(registry):
    """
    경기 시간, 요일, 이동 거리 보정 변수 생성
    """
    # 1. 요일 특성 (주말/평일 구분)
    registry['day_of_week'] = pd.to_datetime(registry['game_date']).dt.dayofweek
    registry['is_weekend'] = registry['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    # 2. 경기 시간 특성 (낮/밤 경기 구분)
    # 18시 이후 경기이면 야간(1), 낮 경기(0)
    registry['is_night_game'] = registry['game_time'].apply(lambda x: 1 if int(str(x)[:2]) >= 18 else 0)
    
    # 3. 이동 거리 보정 (이전 경기 장소와의 거리)
    # 각 팀의 최근 경기 장소 좌표를 트래킹하여 거리 계산
    registry['travel_distance'] = registry.groupby('home_team')['venue_coords'].shift(1).apply(
        lambda x: haversine_distance(x[0], x[1], current_lat, current_lon) if x else 0
    )
    
    return registry
