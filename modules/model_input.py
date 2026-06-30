import pandas as pd
from sklearn.preprocessing import StandardScaler

class ModelInputEngine:
    def __init__(self):
        self.scaler = StandardScaler()

    def prepare_input(self, df_snapshot):
        """
        통합된 피처 스냅샷을 모델 입력값(Scaled)으로 변환합니다.
        """
        # 정규화 대상 컬럼 지정
        features = ['condition_index', 'slope_1d', 'slope_3d', 'slope_7d']
        
        # 데이터 복사 및 스케일링
        df_processed = df_snapshot.copy()
        
        # 주의: 실제 환경에서는 fit을 미리 수행한 scaler를 사용해야 함
        df_processed[features] = self.scaler.fit_transform(df_processed[features])
        
        return df_processed

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    # 7단계에서 나온 통합 데이터 형태 가정
    data = {
        'condition_index': [0.05, -0.02, 0.08],
        'slope_1d': [0.1, -0.05, 0.2],
        'slope_3d': [0.03, -0.01, 0.05],
        'slope_7d': [0.01, 0.02, 0.01]
    }
    df_snapshot = pd.DataFrame(data)
    
    input_engine = ModelInputEngine()
    scaled_data = input_engine.prepare_input(df_snapshot)
    
    print("모델 입력용 정규화된 데이터:")
    print(scaled_data.head())
