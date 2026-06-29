import streamlit as st
import pandas as pd
import ast
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

@st.cache_data
def load_data(analysis_mode="연속적"):
    FILE_NAME = "mlb_full_data_slim.zip"
    if not os.path.exists(FILE_NAME): return pd.DataFrame()
    
    with zipfile.ZipFile(FILE_NAME, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)
    
    # 1. 정제 및 기본 보정
    df.columns = [c.lower().strip() for c in df.columns]
    df = process_weather_features(df)
    df = calculate_bullpen_fatigue(df)
    df = apply_platoon_weights(df)
    
    # 2. 레지스트리 생성
    registry = create_main_registry(df)
    
    # 3. 모든 엔진 통합 병합
    game_metrics = calculate_game_metrics(df)
    registry = registry.merge(game_metrics, on='game_pk', how='left').fillna(0)
    registry = add_schedule_features(registry)
    registry = add_z_score_features(registry)
    registry = add_rolling_features(registry)
    
    return registry
