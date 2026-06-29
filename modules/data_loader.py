import streamlit as st
import pandas as pd
import os
import zipfile

# 기존 모듈 및 신규 모듈 import
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

@st.cache_data
def load_data():
    FILE_NAME = "mlb_full_data_slim.zip"
    if not os.path.exists(FILE_NAME):
        st.error(f"{FILE_NAME} 파일을 찾을 수 없습니다.")
        return pd.DataFrame()
    
    with zipfile.ZipFile(FILE_NAME, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)
    
    df.columns = [c.lower().strip() for c in df.columns]
    
    # 피처 엔지니어링 파이프라인
    df = process_weather_features(df)
    df = calculate_bullpen_fatigue(df)
    df = apply_platoon_weights(df)
    
    # [추가] 작전 성향 지표 및 기존 지표 통합
    df = add_manager_tendency_features(df)
    
    registry = create_main_registry(df)
    game_metrics = calculate_game_metrics(df)
    registry = registry.merge(game_metrics, on='game_pk', how='left').fillna(0)
    
    registry = add_schedule_features(registry)
    registry = add_rivalry_features(registry, df)
    registry = add_z_score_features(registry)
    registry = add_rolling_features(registry)
    
    return registry
