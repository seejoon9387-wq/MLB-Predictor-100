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
from modules.matchup import add_matchup_stats

FILE_NAME = "mlb_full_data_slim.zip"

@st.cache_data
def load_data(analysis_mode="연속적"):
    if not os.path.exists(FILE_NAME):
        raise FileNotFoundError(f"{FILE_NAME} 파일을 찾을 수 없습니다.")
    
    with zipfile.ZipFile(FILE_NAME, 'r') as z:
        file_list = z.namelist()
        with z.open(file_list[0]) as f:
            df = pd.read_csv(f)
    
    # 1. 필수 컬럼 확인 (디버깅용)
    required_col = 'game_pk'
    if required_col not in df.columns:
        # 혹시 이름이 다른 경우(예: game_id) 자동으로 이름 변경 시도
        possible_names = ['game_id', 'game_identifier', 'gameId']
        for name in possible_names:
            if name in df.columns:
                df = df.rename(columns={name: 'game_pk'})
                break
        
        if 'game_pk' not in df.columns:
            st.error(f"오류: 데이터에 필수 컬럼 '{required_col}'이 없습니다. 현재 컬럼: {list(df.columns)}")
            return pd.DataFrame()

    # 2. JSON 정제
    for col in df.columns:
        sample = df[col].dropna()
        if not sample.empty and isinstance(sample.iloc[0], str) and sample.iloc[0].startswith('{'):
            expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else {})
            expanded_df = pd.json_normalize(expanded)
            expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
            df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
            
    # 3. 파이프라인
    df = set_time_index(df)
    df = normalize_text_data(df)
    df = handle_missing_values(df)
    df = remove_outliers(df)
    df = optimize_data_types(df)
    df = add_matchup_stats(df)
    
    # 4. 레지스트리 및 피처 엔지니어링
    if analysis_mode == "독립적":
        registry = pd.concat([create_main_registry(group) for _, group in df.groupby('game_year')])
    else:
        registry = create_main_registry(df)
    
    registry = add_rolling_features(registry)
    
    return registry
