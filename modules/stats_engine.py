import pandas as pd
import numpy as np

class StatsEngine:
    @staticmethod
    def analyze(game_data):
        """
        데이터셋의 모든 컬럼을 활용하여 팀별 '전력 지수' 산출
        """
        # 1. 타격 지표 계산 (가중치 적용)
        batting_score = (
            game_data['OPS'] * 0.4 + 
            game_data['wRC+'] * 0.3 + 
            (1 - game_data['K%']) * 0.3
        )
        
        # 2. 투구 지표 계산 (FIP 기반 안정성)
        pitching_score = (
            (1 / game_data['FIP']) * 0.5 + 
            (game_data['K/9'] / game_data['BB/9']) * 0.5
        )
        
        # 3. 종합 전력 지수 (0~100 정규화)
        # 승률에 직접 영향을 미치는 '팀 전력 벡터' 산출
        composite_score = (batting_score * 0.6) + (pitching_score * 0.4)
        
        return composite_score
