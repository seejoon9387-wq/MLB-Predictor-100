import pandas as pd
import numpy as np

def optimize_data_types(df):
    """
    Pandas API를 사용하여 안전하게 숫자형 컬럼만 찾아 최적화합니다.
    """
    for col in df.columns:
        # pd.api.types를 사용하여 안전하게 숫자형인지 확인
        if pd.api.types.is_numeric_dtype(df[col]):
            col_min = df[col].min()
            col_max = df[col].max()
            
            # 정수형 최적화
            if pd.api.types.is_integer_dtype(df[col]):
                if col_min > np.iinfo(np.int8).min and col_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif col_min > np.iinfo(np.int16).min and col_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif col_min > np.iinfo(np.int32).min and col_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
            
            # 실수형 최적화
            elif pd.api.types.is_float_dtype(df[col]):
                if col_min > np.finfo(np.float32).min and col_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                    
    return df
