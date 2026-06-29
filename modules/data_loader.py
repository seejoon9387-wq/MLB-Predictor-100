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
from modules.sabermetrics import add_defensive_efficiency, add_catcher_impact_features
from modules.manager_tendency import add_manager_tendency_features
from modules.lineup_engine import add_lineup_stability_features
from modules.leverage_engine import add_leverage_weighted_stats
from modules.momentum_engine import add_momentum_features
from modules.pitch_value_engine import add_pitch_value_features
from modules.stamina_engine import add_stamina_and_limit_features # 추가

@st.cache_data
def load_data():
    # ... (데이터 로드 코드 생략) ...
    
    # 순차적 피처 엔지니어링 파이프라인
    df = process_weather_features(df)
    df = calculate_bullpen_fatigue(df)
    df = apply_platoon_weights(df)
    
    # [추가] 투구 한계치 모델링 통합
    df = add_stamina_and_limit_features(df)
    
    # 나머지 엔진 호출
    df = add_pitch_value_features(df)
    df = add_momentum_features(df)
    df = add_leverage_weighted_stats(df)
    df = add_manager_tendency_features(df)
    df = add_lineup_stability_features(df)
    df = add_defensive_efficiency(df)
    df = add_catcher_impact_features(df)
    
    registry = create_main_registry(df)
    game_metrics = calculate_game_metrics(df)
    registry = registry.merge(game_metrics, on='game_pk', how='left').fillna(0)
    
    # ... (병합 및 나머지 피처 추가 동일) ...
    return registry
