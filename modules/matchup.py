import pandas as pd

def add_matchup_stats(df):
    """투수-타자 상성 지표 생성 (원본 데이터 가공용)"""
    matchup_df = df.groupby(['pitcher', 'batter']).agg({
        'woba_value': 'mean',
        'launch_speed': 'mean',
        'at_bat_number': 'count'
    }).rename(columns={
        'woba_value': 'vs_pitcher_woba',
        'launch_speed': 'vs_pitcher_exit_velo',
        'at_bat_number': 'matchup_count'
    })
    
    df = df.merge(matchup_df, on=['pitcher', 'batter'], how='left')
    df['vs_pitcher_woba'] = df['vs_pitcher_woba'].fillna(0.320) # 리그 평균으로 대체
    return df

def get_team_matchup_adjustment(lineup_df):
    """
    오늘의 라인업 df를 받아 팀 단위 상성 보정치를 반환
    """
    if lineup_df.empty:
        return 0.0
        
    avg_woba = lineup_df['vs_pitcher_woba'].mean()
    league_avg_woba = 0.320 
    
    # 상성 보정치 계산 (모델 예측값이 0~1 사이이므로 0.02 내외의 보정이 적절)
    adjustment = (avg_woba - league_avg_woba) * 1.5 
    return max(-0.05, min(0.05, adjustment)) # 과도한 보정 방지
