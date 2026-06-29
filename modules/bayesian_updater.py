# modules/bayesian_updater.py
import numpy as np

def get_bayesian_win_prob(wins, games, league_avg_win_rate=0.5, strength_prior=20):
    """
    Beta 분포를 이용한 승률 보정
    - wins: 현재 승리 수
    - games: 현재 경기 수
    - league_avg_win_rate: 리그 전체 평균 승률(0.5)
    - strength_prior: 사전 분포의 강도(값이 클수록 과거 데이터를 강하게 신뢰)
    """
    # 사전 분포 파라미터 (alpha, beta)
    alpha_prior = league_avg_win_rate * strength_prior
    beta_prior = (1 - league_avg_win_rate) * strength_prior
    
    # 사후 분포 업데이트
    alpha_post = alpha_prior + wins
    beta_post = beta_prior + (games - wins)
    
    # 보정된 승률 (평균값)
    return alpha_post / (alpha_post + beta_post)
