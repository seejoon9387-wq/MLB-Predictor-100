import pandas as pd

def add_matchup_stats(df):
    """
    투수-타자 상성 지표 생성:
    - 동일 투수 vs 동일 타자의 과거 기록을 바탕으로 평균 출루율과 장타력을 계산
    """
    # 투수-타자 페어별 그룹화
    matchup_df = df.groupby(['pitcher', 'batter']).agg({
        'woba_value': 'mean',          # 해당 투수 상대 타자의 평균 WOBA
        'launch_speed': 'mean',       # 해당 투수 상대 타자의 평균 타구 속도
        'at_bat_number': 'count'      # 총 대결 횟수 (샘플 사이즈)
    }).rename(columns={
        'woba_value': 'vs_pitcher_woba',
        'launch_speed': 'vs_pitcher_exit_velo',
        'at_bat_number': 'matchup_count'
    })
    
    # 원본 데이터프레임에 상성 지표 병합
    df = df.merge(matchup_df, on=['pitcher', 'batter'], how='left')
    
    # 대결 횟수가 너무 적으면 데이터 신뢰도가 낮으므로 결측치 처리
    df['vs_pitcher_woba'] = df['vs_pitcher_woba'].fillna(df['woba_value'].mean())
    
    return df
