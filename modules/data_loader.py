import streamlit as st
import pandas as pd
import os
import zipfile

# 모든 엔진 모듈 import
from modules.registry import create_main_registry
from modules.features import add_rolling_features
from modules.weather_processor import process_weather_features
from modules.bullpen import calculate_bullpen_fatigue
from modules.platoon import apply_platoon_weights
from modules.stats_engine import add_z_score_features
from modules.game_metrics import calculate_game_metrics
from modules.schedule_engine import add_schedule_features
from modules.rivalry import add_rivalry_features
from modules.sabermetrics import add_defensive_efficiency, add_catcher_impact_features
from modules.manager_tendency import add_manager_tendency_features
from modules.lineup_engine import add_lineup_stability_features
from modules.leverage_engine import add_leverage_weighted_stats
from modules.momentum_engine import add_momentum_features
from modules.pitch_value_engine import add_pitch_value_features
from modules.stamina_engine import add_stamina_and_limit_features

def add_hitting_quality_features(df):
    batted_balls = df['batted_ball_events'].replace(0, 1)
    df['barrel_rate'] = df['barrel_count'] / batted_balls
    df['hard_hit_rate'] = df['hard_hit_count'] / batted_balls
    df['contact_quality_index'] = (df['barrel_rate'] * 1.5) + (df['hard_hit_rate'] * 0.5)
    df = df.sort_values(['team_id', 'date'])
    df['roll_barrel_rate'] = df.groupby('team_id')['barrel_rate'].transform(lambda x: x.shift(1).rolling(10, min_periods=1).mean())
    return df

@st.cache_data
def load_data():
    FILE_NAME = "mlb_full_data_slim.zip"
    if not os.path.exists(FILE_NAME):
        return pd.DataFrame()
    
    with zipfile.ZipFile(FILE_NAME, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)
    
    df.columns = [c.lower().strip() for c in df.columns]
    if 'home_score' in df.columns and 'away_score' in df.columns:
        df['is_home_win'] = (df['home_score'] > df['away_score']).astype(int)
    
    # 순차적 피처 엔지니어링 (시간 순서 보존)
    df = process_weather_features(df)
    df = calculate_bullpen_fatigue(df)
    df = apply_platoon_features(df)
    df = add_hitting_quality_features(df)
    df = add_stamina_and_limit_features(df)
    df = add_pitch_value_features(df)
    df = add_momentum_features(df)
    df = add_leverage_weighted_stats(df)
    df = add_manager_tendency_features(df)
    df = add_lineup_stability_features(df)
    df = add_defensive_efficiency(df)
    df = add_catcher_impact_features(df)
    
    registry = create_main_registry(df)
    registry = registry.merge(calculate_game_metrics(df), on='game_pk', how='left').fillna(0)
    registry = add_schedule_features(registry)
    registry = add_rivalry_features(registry, df)
    registry = add_z_score_features(registry)
    registry = add_rolling_features(registry)
    
    return registry
