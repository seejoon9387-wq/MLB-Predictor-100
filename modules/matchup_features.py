import pandas as pd

class MatchupFeatureEngine:
    def __init__(self):
        # 범주형 데이터를 수치로 변환하기 위한 딕셔너리 예시
        self.park_factor_map = {'high_offense': 1.1, 'neutral': 1.0, 'low_offense': 0.9}
        self.pitcher_hand_map = {'R': 0, 'L': 1} # 0: 우투, 1: 좌투

    def add_matchup_features(self, df_matchup):
        """
        경기 환경 변수를 모델이 학습 가능한 수치형 데이터로 변환합니다.
        
        Parameters:
        - df_matchup: 경기 매치업 데이터 (park_type, pitcher_hand, temp 등의 컬럼 포함)
        """
        df = df_matchup.copy()
        
        # 구장 효과 변환
        df['park_factor_val'] = df['park_type'].map(self.park_factor_map).fillna(1.0)
        
        # 투수 유형 변환
        df['pitcher_hand_val'] = df['pitcher_hand'].map(self.pitcher_hand_map)
        
        # 날씨 변수 정규화 (예: 온도 - 섭씨 20도 기준 편차)
        df['temp_deviation'] = df['temperature'] - 20.0
        
        return df

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    test_matchup = pd.DataFrame({
        'park_type': ['high_offense', 'neutral', 'low_offense'],
        'pitcher_hand': ['R', 'L', 'R'],
        'temperature': [25, 20, 15]
    })
    
    engine = MatchupFeatureEngine()
    enriched_df = engine.add_matchup_features(test_matchup)
    
    print("환경 변수 변환 결과:")
    print(enriched_df[['park_factor_val', 'pitcher_hand_val', 'temp_deviation']])
