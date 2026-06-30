import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, season_averages):
        """
        season_averages: 사전 계산된 선수별/리그별 평균 데이터프레임
        """
        self.season_averages = season_averages

    def clean_data(self, df_snapshot):
        """
        데이터 정제 및 결측치 발생 시 Fallback 로직 적용
        """
        df_processed = df_snapshot.copy()
        
        # 1. 필수 피처 목록 정의
        required_features = ['condition_index', 'slope_1d', 'slope_3d', 'slope_7d', 'ops']
        
        for feature in required_features:
            # 2. 결측치 식별
            if df_processed[feature].isnull().any():
                print(f"[알림] {feature} 피처 결측 발생. 시즌 평균으로 Fallback 적용.")
                # 3. Fallback Logic: 시즌 평균값으로 대체
                df_processed[feature] = df_processed[feature].fillna(self.season_averages[feature])
        
        return df_processed

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    # 시즌 평균 데이터 시뮬레이션
    avg_data = {'condition_index': 0.0, 'slope_1d': 0.0, 'slope_3d': 0.0, 'slope_7d': 0.0, 'ops': 0.750}
    
    # 결측치가 포함된 데이터
    data = pd.DataFrame({
        'condition_index': [0.05, np.nan, 0.08],
        'slope_1d': [0.1, -0.05, np.nan],
        'slope_3d': [0.03, -0.01, 0.05],
        'slope_7d': [0.01, 0.02, 0.01],
        'ops': [0.8, 0.7, 0.9]
    })
    
    cleaner = DataCleaner(avg_data)
    cleaned_df = cleaner.clean_data(data)
    print("정제 완료된 데이터 (결측치 제거/대체):")
    print(cleaned_df)
