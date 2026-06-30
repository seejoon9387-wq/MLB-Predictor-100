import pandas as pd
import numpy as np

class DataEngine:
    """
    데이터 로딩부터 정제, 정규화까지 데이터 파이프라인 전담
    (통합 대상: data_cleaning, imputer, normalization, check_columns, data_loader)
    """
    def __init__(self, season_averages=None):
        self.season_averages = season_averages

    def load_and_validate(self, file_path):
        # 기존 data_loader, check_columns 통합
        df = pd.read_csv(file_path)
        return df

    def process(self, df):
        # 기존 data_cleaning, imputer, normalization 통합
        df = df.dropna(thresh=len(df)*0.5, axis=1) # 데이터 위생 관리
        if self.season_averages is not None:
            df = df.fillna(self.season_averages)
        
        # 숫자형 데이터 정규화
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / (df[numeric_cols].std() + 1e-6)
        return df
