# modules/data_loader.py
import pandas as pd
import numpy as np

def get_player_stats_fallback(df, player_id, stat_col):
    """Fallback Logic: 특정 데이터 누락 시 해당 선수의 시즌 평균으로 대체"""
    season_avg = df[df['pitcher'] == player_id][stat_col].mean()
    return season_avg if not np.isnan(season_avg) else 0

def load_and_profile(file_path):
    df = pd.read_csv(file_path)
    
    # 선수별 최근 7일 성적 (컨디션 지수 산출을 위한 기초)
    df['game_date'] = pd.to_datetime(df['game_date'])
    df = df.sort_values(['pitcher', 'game_date'])
    
    # 7일 이동 평균 성적 산출 (Rolling)
    df['pitcher_recent_era'] = df.groupby('pitcher')['woba_value'].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean()
    )
    
    # Fallback 적용 예시: release_speed 누락 시 선수 시즌 평균으로 대체
    df['release_speed'] = df.apply(
        lambda row: row['release_speed'] if not pd.isna(row['release_speed']) 
        else get_player_stats_fallback(df, row['pitcher'], 'release_speed'), axis=1
    )
    
    return df
