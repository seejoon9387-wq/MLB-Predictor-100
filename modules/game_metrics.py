import pandas as pd

def calculate_game_metrics(df):
    """
    병살, 도루, 실책 등 세부 운영 지표 산출
    """
    # 1. 이벤트 분류 (events 컬럼 기반)
    df['is_double_play'] = df['events'].apply(lambda x: 1 if 'double_play' in str(x).lower() else 0)
    df['is_stolen_base'] = df['events'].apply(lambda x: 1 if 'stolen_base' in str(x).lower() else 0)
    df['is_error'] = df['events'].apply(lambda x: 1 if 'error' in str(x).lower() else 0)
    
    # 2. 경기별 합계 산출
    metrics = df.groupby('game_pk').agg({
        'is_double_play': 'sum',
        'is_stolen_base': 'sum',
        'is_error': 'sum'
    }).reset_index()
    
    return metrics
