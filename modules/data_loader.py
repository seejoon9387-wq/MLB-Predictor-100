import streamlit as st
import pandas as pd
import ast
import os
import zipfile
from modules.time_series import set_time_index
from modules.text_normalize import normalize_text_data
from modules.imputer import handle_missing_values
from modules.outlier import remove_outliers
from modules.optimizer import optimize_data_types
from modules.registry import create_main_registry
from modules.features import add_rolling_features
from modules.matchup import add_matchup_stats # 신규 추가

FILE_NAME = "mlb_full_data_slim.zip"

@st.cache_data
def load_data(analysis_mode="연속적"):
    # (로드 및 로직 생략 - 이전과 동일)
    # ... 데이터 로드 및 정제 코드 ...
    
    # 파이프라인 적용
    df = set_time_index(df)
    df = normalize_text_data(df)
    df = handle_missing_values(df)
    df = remove_outliers(df)
    df = optimize_data_types(df)
    
    # 1. 상성 지표 생성 (투구 단위 레벨에서 적용)
    df = add_matchup_stats(df)
    
    # 2. 경기 중심 통합 테이블 생성
    registry = create_main_registry(df)
    
    # 3. 이동 평균 지표 적용
    registry = add_rolling_features(registry)
    
    return registry
