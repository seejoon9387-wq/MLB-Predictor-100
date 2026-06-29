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

# 구장 특성 팩터
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
    
    # 1. 컬럼명 정제
    df.columns = [c.lower().strip() for c in df.columns]
    
    # 2. JSON 컬럼 분해
    for col in df.columns:
        if df[col].dtype == 'object' and df[col].astype(str).str.startswith('{').any():
            try:
                expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else {})
                expanded_df = pd.json_normalize(expanded)
                expanded_df.columns = [f"{col}_{subcol}".lower() for subcol in expanded_df.columns]
                df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
            except: continue
    
    # 3. 고급 환경 및 선수 상성 보정 파이프라인
    # 구장 특성
    if 'home_team' in df.columns:
        df['pf_adjusted_home_score'] = df['home_score'] / df['home_team'].map(PARK_FACTORS).fillna(1.0)
    
    # 기상 보정
    df = process_weather_features(df)
    
    # 불펜 피로도 및 가용성
    df = calculate_bullpen_fatigue(df)
    
    # 타자/투수 좌우놀이(Platoon) 보정
    df = apply_platoon_weights(df)
    
    # 4. 레지스트리 생성
    if analysis_mode == "독립적":
        registry = pd.concat([create_main_registry(group) for _, group in df.groupby('game_year')])
    else:
        registry = create_main_registry(df)
    
    # 5. 이동 평균(3, 5, 10, 30경기) 추가 및 최종 결측치 보정
    registry = add_rolling_features(registry)
    
    return registry
