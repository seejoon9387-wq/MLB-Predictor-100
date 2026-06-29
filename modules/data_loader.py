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
from modules.archiver import archive_old_data
from modules.registry import create_main_registry

FILE_NAME = "mlb_full_data_slim.zip"

@st.cache_data
def load_data(analysis_mode="연속적"):
    if not os.path.exists(FILE_NAME):
        raise FileNotFoundError(f"{FILE_NAME} 파일을 찾을 수 없습니다.")
    
    with zipfile.ZipFile(FILE_NAME, 'r') as z:
        file_list = z.namelist()
        with z.open(file_list[0]) as f:
            df = pd.read_csv(f)
    
    for col in df.columns:
        sample = df[col].dropna()
        if not sample.empty and isinstance(sample.iloc[0], str) and sample.iloc[0].startswith('{'):
            expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else {})
            expanded_df = pd.json_normalize(expanded)
            expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
            df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
            
    df = set_time_index(df)
    df = normalize_text_data(df)
    df = handle_missing_values(df)
    df = remove_outliers(df)
    df = optimize_data_types(df)
    df = archive_old_data(df)
    
    # 분석 모드에 따른 분기 처리
    if analysis_mode == "독립적":
        # 시즌별로 그룹화하여 시즌 내 데이터만 유지
        df = df.groupby('game_year').apply(lambda x: x)
    
    registry = create_main_registry(df)
    
    return registry
