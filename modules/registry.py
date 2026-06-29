import pandas as pd

def create_main_registry(df):
    """
    데이터프레임에서 game_pk를 기준으로 경기별 요약 테이블 생성 및 타겟 변수 생성
    """
    # 1. 컬럼명이 소문자인지 확인
    df.columns = [c.lower() for c in df.columns]
    
    if 'game_pk' not in df.columns:
        raise ValueError("registry.py: 데이터에 'game_pk' 컬럼이 없습니다.")
    
    # 2. 경기별 주요 스탯 요약
    registry = df.groupby('game_pk').agg({
        'game_date': 'first',
        'home_team': 'first',
        'away_team': 'first',
        'home_score': 'max',
        'away_score': 'max',
        'launch_speed': 'mean',
        'woba_value': 'mean'
    })
    
    # 3. [추가] 승패 결과 라벨 생성 (타겟 변수)
    # 홈팀 점수가 어웨이팀 점수보다 높으면 1(승리), 아니면 0(패배)
    registry['is_home_win'] = (registry['home_score'] > registry['away_score']).astype(int)
    
    return registry
