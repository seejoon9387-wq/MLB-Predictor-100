# modules/momentum_engine.py
import pandas as pd
import numpy as np

def add_momentum_features(df):
    """
    팀의 연승/연패 기세 및 심리적 모멘텀 지표화
    """
    df = df.sort_values(['team_id', 'date'])
    
    # 1. 기세 점수 (연승은 +, 연패는 -)
    # 최근 10경기 승패 데이터를 가중치 적용하여 합산 (최신 경기일수록 높은 가중치)
    weights = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    df['momentum_score'] = df.groupby('team_id')['is_home_win'].transform(
        lambda x: x.rolling(10, min_periods=1).apply(lambda s: np.dot(s, weights[-len(s):]))
    )
    
    # 2. 기세 가속도 (Momentum Acceleration)
    # 최근 5경기의 기세가 전반적으로 상승 중인지 하락 중인지 확인
    df['momentum_acceleration'] = df.groupby('team_id')['momentum_score'].diff()
    
    # 3. 심리적 압박 지표 (Psychological Pressure)
    # 3연패 이상 시 심리적 압박 지수 급증 (Boolean -> Numeric)
    df['is_losing_streak'] = (df.groupby('team_id')['is_home_win'].rolling(3).sum() == 0).astype(int)
    
    return df
