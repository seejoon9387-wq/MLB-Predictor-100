class Simulator:
    @staticmethod
    def predict_win_probability(home_df, away_df):
        # 홈팀과 원정팀의 종합 전력 지수 비교
        home_score = home_df['batting_index'].mean() + home_df['pitching_index'].mean()
        away_score = away_df['batting_index'].mean() + away_df['pitching_index'].mean()
        
        # 로지스틱 함수를 사용한 승률 변환 (0~1 사이)
        import numpy as np
        win_prob = 1 / (1 + np.exp(-(home_score - away_score)))
        
        return win_prob
