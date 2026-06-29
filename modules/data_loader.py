import streamlit as st
import pandas as pd
import os
import zipfile

# 기존 모듈 및 신규 momentum_engine import
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
from modules.momentum_engine import add_momentum_features # 추가된 모듈

@st.cache_data
def load_data():
    # ... (데이터 로드 부분 동일) ...
    
    # 순차적 피처 엔지니어링 파이프라인
    df = process_weather_features(df)
    df = calculate_bullpen_fatigue(df)
    df = apply_platoon_weights(df)
    
    # [통합] 기세 및 심리적 지표 추가
    df = add_momentum_features(df)
    df = add_leverage_weighted_stats(df)
    df = add_manager_tendency_features(df)
    df = add_lineup_stability_features(df)
    df = add_defensive_efficiency(df)
    df = add_catcher_impact_features(df)
    
    registry = create_main_registry(df)
    # ... (병합 및 나머지 피처 추가 동일) ...
    
    return registry
