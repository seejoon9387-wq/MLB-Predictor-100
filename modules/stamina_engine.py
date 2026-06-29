# modules/stamina_engine.py
import pandas as pd

def add_stamina_and_limit_features(df):
    """
    투구수와 이닝 소화력에 따른 피로도 및 한계치 모델링
    """
    # 1. 투구 한계치 근접도 (현재 투구수 / 투수별 시즌 평균 한계 투구수)
    # 1에 가까울수록 한계치 도달
    df['pitch_limit_ratio'] = df['current_pitch_count'] / df['season_avg_pitch_limit']
    
    # 2. 이닝 소화 효율성 (이닝당 평균 투구수 - NP/IP)
    # 효율이 떨어질수록(값이 클수록) 피로도 급증
    df['efficiency_index'] = df['current_pitch_count'] / df['innings_pitched'].replace(0, 1)
    
    # 3. 누적 피로 지수 (최근 3경기 누적 투구수에 가중치 적용)
    df = df.sort_values(['pitcher_id', 'date'])
    df['cumulative_fatigue'] = df.groupby('pitcher_id')['current_pitch_count'].transform(
        lambda x: x.rolling(3).sum()
    )
    
    # 4. 종합 스태미나 지수 (모델 입력용)
    # 한계치 비율과 효율성을 결합하여 0~1 사이로 정규화
    df['stamina_index'] = (df['pitch_limit_ratio'] * 0.7 + (df['efficiency_index'] / 30) * 0.3)
    
    return df
