import pandas as pd
import numpy as np

class PerformanceNormalizer:
    def __init__(self):
        pass

    def calculate_z_score(self, player_val, league_mean, league_std):
        """
        리그 평균 대비 Z-Score 산출
        Z = (선수 성적 - 리그 평균) / 리그 표준편차
        """
        if league_std == 0:
            return 0.0
        return (player_val - league_mean) / league_std

    def normalize_player_performance(self, df_player, df_league_stats, feature='ops'):
        """
        선수의 일자별 성적을 해당 일자의 리그 평균으로 정규화합니다.
        
        Parameters:
        - df_player: 선수 데이터프레임 (date 컬럼 포함)
        - df_league_stats: 리그 평균 데이터프레임 (date, mean_ops, std_ops 컬럼 포함)
        """
        # 날짜별로 병합
        merged = pd.merge(df_player, df_league_stats, on='date', how='left')
        
        # Z-Score 컬럼 생성
        merged[f'{feature}_zscore'] = merged.apply(
            lambda row: self.calculate_z_score(row[feature], row[f'mean_{feature}'], row[f'std_{feature}']), 
            axis=1
        )
        
        return merged

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    # 가상 리그 데이터 (date별 평균과 표준편차)
    league_data = pd.DataFrame({
        'date': ['2026-06-01', '2026-06-02'],
        'mean_ops': [0.720, 0.725],
        'std_ops': [0.05, 0.05]
    })
    
    # 선수 가상 데이터
    player_data = pd.DataFrame({
        'date': ['2026-06-01', '2026-06-02'],
        'ops': [0.850, 0.700]
    })
    
    normalizer = PerformanceNormalizer()
    normalized_df = normalizer.normalize_player_performance(player_data, league_data, feature='ops')
    
    print("정규화된 데이터 결과:")
    print(normalized_df[['date', 'ops', 'ops_zscore']])
