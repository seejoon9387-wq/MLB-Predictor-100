import pandas as pd
import numpy as np

def optimize_data_types(df):
    """
    데이터 타입 최적화:
    - 수치형 데이터(int, float)만 대상으로 하여 메모리 최적화 수행
    - 문자열이나 기타 타입은 건드리지 않아 데이터 타입 오류 방지
    """
    for col in df.columns:
        # 1. 컬럼의 현재 타입 확인
        col_type = df[col].dtype
        
        # 2. 'number' 계열(int 또는 float)인지 확인 (object, string 등은 제외)
        if np.issubdtype(col_type, np.number):
            col_min = df[col].min()
            col_max = df[col].max()
            
            # 정수형(Integer)인 경우
            if np.issubdtype(col_type, np.integer):
                if col_min > np.iinfo(np.int8).min and col_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif col_min > np.iinfo(np.int16).min and col_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif col_min > np.iinfo(np.int32).min and col_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                # int64는 그대로 유지
            
            # 실수형(Float)인 경우
            else:
                if col_min > np.finfo(np.float32).min and col_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                # float64는 그대로 유지
                    
    return df
