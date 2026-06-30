import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, min_pa=5):
        # min_pa: 통계적 유의성을 확보하기 위한 최소 타석 수 기준
        self.min_pa = min_pa

    def handle_outliers(self, df, feature='ops'):
        """
        IQR(Interquartile Range) 방식을 사용하여 극단치를 제거합니다.
        """
        Q1 = df[feature].quantile(0.25)
        Q3 = df[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        return df[(df[feature] >= lower_bound) & (df[feature] <= upper_bound)]

    def clean_data(self, df, pa_col='pa'):
        """
        데이터 품질 정제 메인 프로세스
        1. 최소 타석 미만 데이터 제외
        2. 이상치 제거
        """
        # 1. 최소 타석 조건 필터링
        df_cleaned = df[df[pa_col] >= self.min_pa].copy()
        
        # 2. 결측치 처리 (직전 값으로 보간)
        df_cleaned = df_cleaned.ffill()
        
        # 3. 이상치 제거 (IQR 기준)
        df_final = self.handle_outliers(df_cleaned)
        
        return df_final

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    raw_data = pd.DataFrame({
        'pa': [1, 10, 15, 2, 20],  # 타석 수
        'ops': [0.100, 0.750, 0.800, 2.000, 0.720]  # OPS (2.000은 이상치 가정)
    })
    
    cleaner = DataCleaner(min_pa=5)
    cleaned_df = cleaner.clean_data(raw_data)
    
    print("정제된 데이터 결과:")
    print(cleaned_df)
