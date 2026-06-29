import pandas as pd

def create_main_registry(df):
    """
    데이터프레임에서 game_pk를 기준으로 경기별 요약 테이블 생성
    """
    # 1. 컬럼명이 소문자인지 확인 (데이터 로더에서 이미 소문자화했지만 안전을 위해)
    df.columns = [c.lower() for c in df.columns]
    
    if 'game_pk' not in df.columns:
        raise ValueError(f"registry.py: 데이터에 'game_pk' 컬럼이 없습니다. 현재 컬럼: {list(df.columns)}")
    
    # 2. 경기별 주요 스탯 요약 (피처 엔지니어링용)
    registry = df.groupby('game_pk').agg({
        'game_date': 'first',
        'home_team': 'first',
        'away_team': 'first',
        'home_score': 'max',
        'away_score': 'max',
        'launch_speed': 'mean',
        'woba_value': 'mean'
    })
    
    return registry
