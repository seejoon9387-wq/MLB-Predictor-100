import numpy as np
from scipy.stats import beta

class BayesianInferenceEngine:
    def __init__(self, alpha_prior=10, beta_prior=30):
        # 선수의 시즌 평균 기량을 사전 분포(Beta 분포)의 파라미터로 가정
        self.alpha_prior = alpha_prior
        self.beta_prior = beta_prior

    def get_posterior_distribution(self, hits, at_bats, condition_multiplier=1.0):
        """
        베이즈 추론을 통해 성적의 확률 분포를 업데이트합니다.
        condition_multiplier: 컨디션 지수를 반영한 우도 가중치
        """
        # 관측 데이터 반영 (우도 업데이트)
        alpha_post = self.alpha_prior + (hits * condition_multiplier)
        beta_post = self.beta_prior + (at_bats - hits) * condition_multiplier
        
        return alpha_post, beta_post

    def get_expected_performance(self, alpha_post, beta_post):
        """사후 분포의 기대값(평균) 산출"""
        return alpha_post / (alpha_post + beta_post)

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    inference_engine = BayesianInferenceEngine()
    
    # 예: 최근 10타석에서 3안타를 쳤고, 컨디션 지수(1.2)가 반영된 경우
    hits, at_bats = 3, 10
    alpha, beta_val = inference_engine.get_posterior_distribution(hits, at_bats, condition_multiplier=1.2)
    expected_val = inference_engine.get_expected_performance(alpha, beta_val)
    
    print(f"베이즈 추론 기반 기대 성적: {expected_val:.4f}")
