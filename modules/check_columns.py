import pandas as pd
import numpy as np

def validate_data(file_path):
    print("--- [데이터 무결성 검증 시작] ---")
    df = pd.read_csv(file_path)
    
    # 1. 필수 컬럼 확인
    required_cols = ['pitch_type', 'release_speed', 'woba_value', 'game_date']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"오류: 필수 컬럼 누락 -> {missing}")
        return False
    
    # 2. 결측치 및 이상치 요약
    print(f"총 행 개수: {len(df)}")
    print(f"결측치 확인:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    
    # 3. 데이터 타입 검사 (타입 혼재 방지)
    print("--- 데이터 타입 무결성 ---")
    print(df.dtypes.value_counts())
    
    print("--- [검증 완료] ---")
    return True

if __name__ == "__main__":
    validate_data(r'C:\Users\pc\Desktop\github\mlb_master_final.csv')
