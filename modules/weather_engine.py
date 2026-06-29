# modules/weather_engine.py
import numpy as np

def get_air_density_factor(temp_f):
    """
    온도에 따른 공기 밀도 계수 (기준 70도 화씨)
    온도가 높으면 공기 밀도가 낮아져 타구 비거리가 증가함
    """
    return 1 + (temp_f - 70) * 0.0025

def get_wind_effect(wind_speed, wind_direction_deg, home_team_side):
    """
    풍향 및 풍속이 타구에 미치는 효과 계산
    - wind_direction_deg: 바람이 불어오는 각도
    - home_team_side: 홈팀 타석 방향 (0도 기준)
    """
    # 0도(중앙 펜스)를 기준으로 한 각도차 계산
    angle_diff = np.radians(wind_direction_deg - home_team_side)
    wind_impact = wind_speed * np.cos(angle_diff)
    return wind_impact * 0.15 # 비거리 보정 계수

def apply_climate_adjustment(df):
    # 온도 보정: 온도가 높을수록 득점 확률 상승
    df['temp_factor'] = df['temp_f'].apply(get_air_density_factor)
    
    # 풍향 보정: 바람 영향 추가
    df['wind_factor'] = df.apply(
        lambda x: get_wind_effect(x['wind_speed'], x['wind_dir_deg'], 0), axis=1
    )
    
    # 최종 확률 보정 (기상 영향 반영)
    df['climate_adjusted_prob'] = df['home_win_exp'] * df['temp_factor'] + df['wind_factor']
    return df
