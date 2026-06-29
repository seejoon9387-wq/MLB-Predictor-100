import streamlit as st
import pandas as pd
import os
import zipfile

# 기존 모듈 import (modules 폴더 내에 이 파일들이 존재해야 합니다)
from modules.registry import create_main_registry
from modules.features import add_rolling_features
from modules.weather_processor import process_weather_features
from modules.bullpen import calculate_bullpen_fatigue
from modules.platoon import apply_platoon_weights
from modules.stats_engine import add_z_score_features
from modules.game_metrics import calculate_game_metrics
from modules.schedule_engine import add_schedule_features
from modules.rivalry import add_rivalry_features

def add_hitting_quality_features(df):
    """배럴 및 강한 타구 기반 타격력 지표 추가"""
    batted_balls = df['batted_ball_events'].replace(0, 1)
    df['barrel_rate'] = df['barrel_count'] / batted_balls
    df['hard_hit_rate'] = df['hard_hit_count'] / batted_balls
    df['contact_quality_index'] = (df['barrel_rate'] * 1.5) + (df['hard_hit_rate'] * 0.5)
    
    # 이동 평균 추가 (팀별 날짜 순 정렬 필수)
    df = df.sort_values(['team_id', 'date'])
    df['roll_barrel_rate'] = df.groupby('team_id')['barrel_rate'].transform(lambda x: x.rolling(10, min_periods=1).mean())
    return df

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
    
    if 'home_score' in df.columns and 'away_score' in df.columns:
        df['is_home_win'] = (df['home_score'] > df['away_score']).astype(int)
    
    # 피처 엔진 적용
    df = process_weather_features(df)
    df = calculate_bullpen_fatigue(df)
    df = apply_platoon_weights(df)
    df = add_hitting_quality_features(df)
    
    # 레지스트리 및 최종 통합
    registry = create_main_registry(df)
    game_metrics = calculate_game_metrics(df)
    registry = registry.merge(game_metrics, on='game_pk', how='left').fillna(0)
    registry = add_schedule_features(registry)
    registry = add_rivalry_features(registry, df)
    registry = add_z_score_features(registry)
    registry = add_rolling_features(registry)
    
    return registry
