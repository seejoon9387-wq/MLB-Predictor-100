import pandas as pd

class StatsEngine:
    @staticmethod
    def calculate_team_strength(df):
        """
        데이터프레임의 핵심 컬럼을 활용해 승리 기여 지수(Win Contribution) 산출
        """
        # 타격 효율: wOBA와 발사각/속도의 결합
        df['batting_index'] = (df['woba_value'] * 0.5) + (df['launch_speed'] * 0.01) + (df['launch_angle'] * 0.005)
        
        # 투구 효율: FIP와 구속(effective_speed)의 결합
        df['pitching_index'] = (1 / (df['era'] + 0.001)) + (df['effective_speed'] * 0.02) - (df['whip'] * 0.5)
        
        return df[['team', 'batting_index', 'pitching_index']]
