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

PARK_FACTORS = {'Fenway Park': 1.05, 'Dodger Stadium': 0.95, 'Yankee Stadium': 1.02}

@st.cache_data
def load_data(analysis_mode="연속적"):
    FILE_NAME = "mlb_full_data_slim.zip"
    if not os.path.exists(FILE_NAME):
        st.error(f"{FILE_NAME} 파일을 찾을 수 없습니다.")
        return pd.DataFrame()
    
    with zipfile.ZipFile(FILE_NAME, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)
    
    # 1. 기본 전처리
    df.columns = [c.lower().strip() for c in df.columns]
    for col in df.columns:
        if df[col].dtype == 'object' and df[col].astype(str).str.startswith('{').any():
            try:
                expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else {})
                expanded_df = pd.json_normalize(expanded)
                expanded_df.columns = [f"{col}_{subcol}".lower() for subcol in expanded_df.columns]
                df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
            except: continue
    
    # 2. 보정 엔진 적용
    if 'home_team' in df.columns:
        df['pf_adjusted_home_score'] = df['home_score'] / df['home_team'].map(PARK_FACTORS).fillna(1.0)
    
    df = process_weather_features(df)
    df = calculate_bullpen_fatigue(df)
    df = apply_platoon_weights(df)
    
    # 3. 경기 운영 지표 산출
    game_metrics = calculate_game_metrics(df)
    
    # 4. 레지스트리 병합
    if analysis_mode == "독립적":
        registry = pd.concat([create_main_registry(group) for _, group in df.groupby('game_year')])
    else:
        registry = create_main_registry(df)
    
    registry = registry.merge(game_metrics, on='game_pk', how='left').fillna(0)
    
    # 5. 최종 통계 피처링
    registry = add_z_score_features(registry)
    registry = add_rolling_features(registry)
    
    return registry
