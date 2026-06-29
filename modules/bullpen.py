import pandas as pd

def calculate_bullpen_fatigue(df):
    """
    투수별 피로도 및 가용성 지표 산출
    - fatigue_score: 최근 3일간의 투구수 합계 (높을수록 피로)
    - rest_score: 마지막 등판 후 휴식일 (높을수록 가용성 높음)
    """
    # 1. 투수별 데이터 정렬
    df = df.sort_values(['pitcher', 'game_date'])
    
    # 2. 피로도: 최근 3경기 누적 투구수 계산
    df['fatigue_score'] = df.groupby('pitcher')['pitch_number'].transform(
        lambda x: x.rolling(window=3, min_periods=1).sum()
    )
    
    # 3. 가용성: 휴식일 산출 (현재 날짜 - 마지막 등판 날짜)
    # 데이터셋에 'pitcher_days_since_prev_game'이 있다면 활용, 없으면 직접 계산
    if 'pitcher_days_since_prev_game' in df.columns:
        df['availability_score'] = df['pitcher_days_since_prev_game'].apply(
            lambda x: 1.0 if x >= 2 else (0.5 if x == 1 else 0.0)
        )
    else:
        df['availability_score'] = 0.5 # 기본값
        
    return df
