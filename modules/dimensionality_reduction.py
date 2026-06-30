import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class DimensionalityReducer:
    def __init__(self, n_components=0.95):
        # n_components=0.95는 전체 분산의 95%를 보존하는 주성분을 자동으로 선택
        self.pca = PCA(n_components=n_components)
        self.scaler = StandardScaler()

    def analyze_correlation(self, df):
        """피처 간 상관관계 행렬 분석"""
        corr_matrix = df.corr()
        return corr_matrix

    def reduce_dimensions(self, df):
        """PCA를 통한 차원 축소 수행"""
        scaled_data = self.scaler.fit_transform(df)
        reduced_data = self.pca.fit_transform(scaled_data)
        return reduced_data

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    # 임의의 고차원 데이터프레임 가정
    data = pd.DataFrame({
        'ops': [0.7, 0.8, 0.6],
        'condition_index': [0.05, 0.08, -0.02],
        'temp_deviation': [5, 0, -5],
        'pitcher_hand': [0, 1, 0]
    })
    
    reducer = DimensionalityReducer()
    
    # 상관관계 분석
    print("상관관계 행렬:")
    print(reducer.analyze_correlation(data))
    
    # 차원 축소
    reduced = reducer.reduce_dimensions(data)
    print(f"\n축소된 데이터 형태: {reduced.shape}")
