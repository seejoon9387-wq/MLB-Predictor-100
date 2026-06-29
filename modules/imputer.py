import pandas as pd
import numpy as np

def handle_missing_values(df):
    """
    결측치 처리 알고리즘:
    1. 수치형 데이터: 중앙값(Median)으로 대체 (이상치에 강함)
    2. 범주형(텍스트) 데이터: 'unknown'으로 대체
    """
    for col in df.columns:
        # 1. 수치형 컬럼 처리
        if pd.api.types.is_numeric_dtype(df[col]):
            if df[col].isnull().sum() > 0:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
        
        # 2. 범주형(텍스트) 컬럼 처리
        else:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna('unknown')
                
    return df
