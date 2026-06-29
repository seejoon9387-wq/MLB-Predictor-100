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
from modules.rivalry import add_rivalry_features

@st.cache_data
def load_data(analysis_mode="연속적"):
    FILE_NAME = "mlb_full_data_slim.zip"
    if not os.path.exists(FILE_NAME):
        st.error(f"{FILE_NAME} 파일을 찾을 수 없습니다.")
        return pd.DataFrame()
    
    with zipfile.ZipFile(FILE_NAME, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)
    
    # 1. 컬럼명 정제
    df.columns = [c.lower().strip() for c in df.columns]
    
    # 2. 타깃 변수 사전 정의 (오류 방지)
    if 'home_score' in df.columns and 'away_score' in df.columns:
        df['is_home_win'] = (df['home_score'] > df['away_score']).astype(int)
    
    # 3. 데이터 로딩 및 피처 엔진 적용
    df = process_weather_features(df)
    df = calculate_bullpen_fatigue(df)
    df = apply_platoon_weights(df)
    
    # 4. 레지스트리 생성
    registry = create_main_registry(df)
    
    # 5. 모든 지표 통합 병합
    game_metrics = calculate_game_metrics(df)
    registry = registry.merge(game_metrics, on='game_pk', how='left').fillna(0)
    registry = add_schedule_features(registry)
    registry = add_rivalry_features(registry, df)
    registry = add_z_score_features(registry)
    registry = add_rolling_features(registry)
    
    return registry
