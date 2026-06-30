import numpy as np

def get_climate_adjustment(weather_data):
    """
    기상 정보(온도, 풍속, 풍향)를 받아 승률 보정치를 반환
    weather_data 구조: {'temp_f': int, 'wind_speed': int, 'wind_dir_deg': int}
    """
    temp_f = weather_data.get('temp_f', 70)
    wind_speed = weather_data.get('wind_speed', 0)
    wind_dir = weather_data.get('wind_dir_deg', 0)
    
    # 1. 온도에 따른 공기 밀도 효과 (비거리 증가)
    temp_factor = (temp_f - 70) * 0.001  # 승률 변화율로 스케일 조정
    
    # 2. 바람 영향 (홈런/비거리 영향)
    angle_diff = np.radians(wind_dir - 0) # 0도(중앙 펜스) 기준
    wind_impact = wind_speed * np.cos(angle_diff) * 0.002
    
    adjustment = temp_factor + wind_impact
    return max(-0.03, min(0.03, adjustment)) # 과도한 보정 방지
