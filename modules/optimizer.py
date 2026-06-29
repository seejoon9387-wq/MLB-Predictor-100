import pandas as pd
import numpy as np

def optimize_data_types(df):
    """
    데이터 타입 최적화:
    - 수치형 데이터의 타입을 정밀도에 맞춰 축소 (int64 -> int32/16, float64 -> float32)
    - 메모리 점유율을 대폭 감소시킴
    """
    for col in df.columns:
        col_type = df[col].dtype
        
        # 1. 수치형 데이터 최적화
        if np.issubdtype(col_type, np.number):
            col_min = df[col].min()
            col_max = df[col].max()
            
            # 정수형 최적화
            if np.issubdtype(col_type, np.integer):
                if col_min > np.iinfo(np.int8).min and col_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif col_min > np.iinfo(np.int16).min and col_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif col_min > np.iinfo(np.int32).min and col_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                else:
                    df[col] = df[col].astype(np.int64)
            # 실수형 최적화
            else:
                if col_min > np.finfo(np.float32).min and col_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
                    
    return df
