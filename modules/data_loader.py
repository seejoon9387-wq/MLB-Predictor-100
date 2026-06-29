import streamlit as st
import pandas as pd
import ast
import os
import zipfile
from modules.time_series import set_time_index
from modules.text_normalize import normalize_text_data
from modules.imputer import handle_missing_values
from modules.optimizer import optimize_data_types

FILE_NAME = "mlb_full_data_slim.zip"

@st.cache_data
def load_data():
    if not os.path.exists(FILE_NAME):
        raise FileNotFoundError(f"{FILE_NAME} 파일을 찾을 수 없습니다.")
    
    with zipfile.ZipFile(FILE_NAME, 'r') as z:
        file_list = z.namelist()
        with z.open(file_list[0]) as f:
            df = pd.read_csv(f)
    
    # JSON 정제 로직
    for col in df.columns:
        sample = df[col].dropna()
        if not sample.empty and isinstance(sample.iloc[0], str) and sample.iloc[0].startswith('{'):
            expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else {})
            expanded_df = pd.json_normalize(expanded)
            expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
            df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
            
    # 엔진 진화 파이프라인 적용
    df = set_time_index(df)           # 1. 시계열 인덱싱
    df = normalize_text_data(df)      # 2. 텍스트 정규화
    df = handle_missing_values(df)    # 3. 결측치 처리
    df = optimize_data_types(df)      # 4. 메모리 최적화 (신규)
    
    return df
