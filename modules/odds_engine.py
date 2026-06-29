# modules/odds_engine.py
import pandas as pd

def add_odds_market_features(df):
    """
    시장 배당 변화를 통한 정보성 피처 추출
    """
    # 1. 배당 변화율 (초기 배당 대비 현재 배당 변화)
    df['odds_movement'] = (df['current_home_odds'] - df['opening_home_odds']) / df['opening_home_odds']
    
    # 2. 시장 기대 승률 (배당 역수) 및 모델 예측값과의 차이
    df['market_win_prob'] = 1 / df['current_home_odds']
    df['odds_discrepancy'] = df['market_win_prob'] - df['model_base_win_prob']
    
    # 3. 배당 변화 가속도 (직전 3경기 시장 평가 추이)
    df['odds_trend'] = df.groupby('team_id')['odds_movement'].transform(lambda x: x.diff().rolling(3).mean())
    
    return df
