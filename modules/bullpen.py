import pandas as pd

def calculate_bullpen_fatigue(df):
    """
    투수의 최근 등판 기록을 바탕으로 피로도 점수 산출
    """
    if 'pitcher' not in df.columns or 'pitch_number' not in df.columns:
        df['fatigue_score'] = 0.0
        df['availability_score'] = 1.0
        return df

    df = df.sort_values(['pitcher', 'game_date'])
    
    # 최근 3경기 누적 투구수로 피로도 점수 산출
    df['fatigue_score'] = df.groupby('pitcher')['pitch_number'].transform(
        lambda x: x.rolling(window=3, min_periods=1).sum()
    )
    
    # 휴식일 기반 가용성 산출
    if 'pitcher_days_since_prev_game' in df.columns:
        df['availability_score'] = df['pitcher_days_since_prev_game'].apply(
            lambda x: 1.0 if x >= 2 else (0.5 if x == 1 else 0.0)
        )
    else:
        df['availability_score'] = 0.5
        
    return df
