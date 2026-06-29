# modules/inefficiency_engine.py
import pandas as pd

def detect_market_bias(df):
    """
    시장 비효율성 및 북메이커 편향 분석
    - model_prob: AI 모델이 계산한 순수 승리 확률
    - market_prob: 북메이커가 제공한 배당 역수(시장 확률)
    """
    # 1. 북메이커의 내재 확률(Implied Probability) 계산
    # 배당이 1.5면 확률은 1/1.5 = 66.6%
    df['market_prob'] = 1 / df['current_home_odds']
    
    # 2. 모델 예측값과 시장 확률의 차이 (비효율성 점수)
    # 양수면 북메이커가 해당 팀을 과소평가(역배당 효율 발생)
    df['inefficiency_score'] = df['model_base_win_prob'] - df['market_prob']
    
    # 3. Public Betting Bias 추정
    # 시장 확률이 모델보다 훨씬 높다면 대중의 인기가 배당을 왜곡했다고 판단
    df['is_public_bias'] = df['inefficiency_score'] < -0.05
    
    return df
