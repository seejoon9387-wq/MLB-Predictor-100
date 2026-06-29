import streamlit as st
import pandas as pd
import os
import zipfile

from modules.registry import create_main_registry
from modules.features import add_rolling_features
from modules.weather_processor import process_weather_features
from modules.bullpen import calculate_bullpen_fatigue
from modules.platoon import apply_platoon_weights
from modules.stats_engine import add_z_score_features
from modules.game_metrics import calculate_game_metrics
from modules.schedule_engine import add_schedule_features
from modules.rivalry import add_rivalry_features
from modules.sabermetrics import calculate_sabermetrics

@st.cache_data
def load_data(analysis_mode="연속적"):
    FILE_NAME = "mlb_full_data_slim.zip"
    if not os.path.exists(FILE_NAME):
        return pd.DataFrame()
    
    with zipfile.ZipFile(FILE_NAME, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)
    
    df.columns = [c.lower().strip() for c in df.columns]
    if 'home_score' in df.columns and 'away_score' in df.columns:
        df['is_home_win'] = (df['home_score'] > df['away_score']).astype(int)
    
    # 1. 보정 및 지표 산출 엔진 적용
    df = process_weather_features(df)
    df = calculate_bullpen_fatigue(df)
    df = apply_platoon_weights(df)
    
    # 2. 레지스트리 생성 및 병합
    registry = create_main_registry(df)
    
    # 3. 모든 엔진 통합 (Metrics, Schedule, Rivalry, Sabermetrics)
    registry = registry.merge(calculate_game_metrics(df), on='game_pk', how='left').fillna(0)
    registry = registry.merge(calculate_sabermetrics(df), on='game_pk', how='left').fillna(0)
    registry = add_schedule_features(registry)
    registry = add_rivalry_features(registry, df)
    
    # 4. 최종 통계 피처링
    registry = add_z_score_features(registry)
    registry = add_rolling_features(registry)
    
    return registry
