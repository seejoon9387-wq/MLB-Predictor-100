import streamlit as st
import pandas as pd
import ast
import os
import zipfile

# 내부 모듈 로드
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
    
    # 1. 데이터 정제
    df.columns = [c.lower().strip() for c in df.columns]
    
    # 2. 보정 엔진 일괄 적용
    df = process_weather_features(df)
    df = calculate_bullpen_fatigue(df)
    df = apply_platoon_weights(df)
    
    # 3. 레지스트리 및 경기 지표 병합
    registry = create_main_registry(df)
    game_metrics = calculate_game_metrics(df)
    registry = registry.merge(game_metrics, on='game_pk', how='left').fillna(0)
    
    # 4. 외부 환경 및 천적 관계 매핑
    registry = add_schedule_features(registry)
    registry = add_rivalry_features(registry, df)
    
    # 5. 최종 통계 지표 처리
    registry = add_z_score_features(registry)
    registry = add_rolling_features(registry)
    
    return registry
