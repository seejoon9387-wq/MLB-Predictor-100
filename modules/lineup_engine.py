# modules/lineup_engine.py
import pandas as pd

def add_lineup_stability_features(df):
    """
    라인업 안정성(최근 10경기 라인업 유지율) 및 핵심 선수 결장 변수
    """
    # 1. 라인업 안정성: 최근 10경기 라인업 변경 횟수의 역수
    # (변경이 적을수록 값이 높음)
    df = df.sort_values(['team_id', 'date'])
    df['lineup_change_count'] = df.groupby('team_id')['lineup_id'].diff().ne(0).rolling(10, min_periods=1).sum()
    df['lineup_stability'] = 1 / (df['lineup_change_count'] + 1)
    
    # 2. 핵심 선수 부상 변수: WAR 상위 3명의 결장 여부
    # 결장 시 0, 출전 시 1 (데이터에 is_active 플래그가 있다고 가정)
    df['key_player_absent'] = (df['is_key_player'] == 1) & (df['is_active'] == 0)
    df['absent_impact_score'] = df.groupby('game_pk')['key_player_absent'].transform('sum')
    
    return df
