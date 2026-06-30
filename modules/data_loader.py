# modules/data_loader.py
import pandas as pd
import numpy as np
import os

def load_data_by_year(year, base_path=r'C:\Users\pc\Desktop\github'):
    """연도별로 데이터를 로드하고 Fallback Logic을 적용하는 데이터 로더"""
    file_path = os.path.join(base_path, 'mlb_master_final.csv')
    
    # 1. 특정 연도 데이터만 chunking 또는 필터링하여 로드
    # 메모리 효율을 위해 iterator 사용 가능
    df = pd.read_csv(file_path)
    df = df[df['game_year'] == year]
    
    # 2. 결측치에 대한 Fallback Logic (시즌 평균 적용)
    # 수치형 컬럼의 결측치를 해당 선수(pitcher)의 연도별 평균으로 보정
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df.groupby('pitcher')[col].transform('mean'))
            
    return df

def get_player_condition(df, player_id, days=7):
    """특정 선수의 최근 N일간 성적(컨디션 지수) 산출"""
    player_data = df[df['pitcher'] == player_id].sort_values('game_date')
    return player_data['woba_value'].rolling(window=days).mean().iloc[-1]
