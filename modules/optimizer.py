import pandas as pd
import numpy as np

def optimize_data_types(df):
    """
    데이터 타입 최적화:
    - 수치형 데이터만 대상으로 하여 메모리 최적화 수행
    - 문자열(object)이나 범주형(category) 데이터는 건드리지 않아 오류 방지
    """
    for col in df.columns:
        col_type = df[col].dtype
        
        # 오직 숫자(int, float)인 경우에만 최적화 수행
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
                # int64는 그대로 유지
            
            # 실수형 최적화
            else:
                if col_min > np.finfo(np.float32).min and col_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                # float64는 그대로 유지
                    
    return df
