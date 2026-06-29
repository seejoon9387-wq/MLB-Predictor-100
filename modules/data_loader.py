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
        st.error(f"{FILE_NAME} 파일을 찾을 수 없습니다.")
        return pd.DataFrame()
    
    with zipfile.ZipFile(FILE_NAME, 'r') as z:
        file_list = z.namelist()
        with z.open(file_list[0]) as f:
            df = pd.read_csv(f)
            
    # [핵심 수정] 컬럼 이름 강제 보존 (대소문자 무시)
    df.columns = [col.lower().strip() for col in df.columns]
    
    # 1. JSON 정제 (여기서 컬럼이 깨질 가능성이 높음)
    for col in df.columns:
        sample = df[col].dropna()
        if not sample.empty and isinstance(sample.iloc[0], str) and sample.iloc[0].startswith('{'):
            try:
                expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else {})
                expanded_df = pd.json_normalize(expanded)
                expanded_df.columns = [f"{col}_{subcol}".lower() for subcol in expanded_df.columns]
                df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
            except:
                continue
    
    # 2. 필수 컬럼 확인
    if 'game_pk' not in df.columns:
        st.error(f"필수 컬럼 'game_pk'가 손실되었습니다. 현재 컬럼: {list(df.columns)}")
        return pd.DataFrame()

    # 3. 파이프라인 적용
    df = set_time_index(df)
    df = normalize_text_data(df)
    df = handle_missing_values(df)
    df = remove_outliers(df)
    df = optimize_data_types(df)
    df = add_matchup_stats(df)
    
    # 4. 레지스트리 생성
    try:
        if analysis_mode == "독립적":
            # 시즌별 처리 시 game_pk가 살아있는지 확인
            registry = pd.concat([create_main_registry(group) for _, group in df.groupby('game_year')])
        else:
            registry = create_main_registry(df)
        
        registry = add_rolling_features(registry)
    except Exception as e:
        st.error(f"레지스트리 생성 중 오류: {e}")
        return pd.DataFrame()
    
    return registry
