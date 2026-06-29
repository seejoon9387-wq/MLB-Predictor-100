# modules/manager_tendency.py
import pandas as pd

def add_manager_tendency_features(df):
    """
    감독의 작전 성향을 최근 30경기 이동 평균으로 수치화
    """
    # 1. 특정 작전 수행 빈도 계산 (경기당)
    df['aggressiveness_index'] = (
        df['stolen_base_attempts'] * 1.5 + 
        df['hit_and_run_attempts'] * 1.2 - 
        df['sacrifice_bunt_attempts'] * 0.8
    )
    
    # 2. 이동 평균을 통한 성향 지수 도출 (30경기 기준)
    df = df.sort_values(['manager_id', 'date'])
    df['manager_aggressiveness'] = df.groupby('manager_id')['aggressiveness_index'].transform(
        lambda x: x.rolling(30, min_periods=1).mean()
    )
    
    return df
