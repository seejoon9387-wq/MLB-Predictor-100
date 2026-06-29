import pandas as pd

def create_main_registry(df):
    """
    경기별 데이터 요약:
    - game_pk를 기준으로 경기당 정보를 집계
    - 승패 여부, 최종 점수, 공격/수비 지표 요약
    """
    # 1. 경기별 핵심 지표 집계
    registry = df.groupby('game_pk').agg({
        'home_team': 'first',
        'away_team': 'first',
        'home_score': 'max',
        'away_score': 'max',
        'game_year': 'first',
        'launch_speed': 'mean',  # 경기 평균 타구 속도
        'release_spin_rate': 'mean' # 경기 평균 투구 회전수
    })
    
    # 2. 경기 승패(Target) 컬럼 생성
    registry['home_win'] = (registry['home_score'] > registry['away_score']).astype(int)
    
    return registry
