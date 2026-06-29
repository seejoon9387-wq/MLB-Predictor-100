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
    
    # 1. 컬럼명 정제 및 자동 매핑
    # 데이터셋마다 'game_pk' 명칭이 다를 수 있으므로 자동 변환
    target_map = {
        'game_pk': ['game_pk', 'game_id', 'game', 'game_identifier', 'gameId', 'game_ID'],
        'pitcher': ['pitcher', 'pitcher_id', 'pitcherId'],
        'batter': ['batter', 'batter_id', 'batterId']
    }
    
    for real_name, variants in target_map.items():
        for variant in variants:
            if variant in df.columns:
                df = df.rename(columns={variant: real_name})
                break
    
    # 만약 'game_pk'가 여전히 없다면 디버깅을 위해 보여줌
    if 'game_pk' not in df.columns:
        st.error(f"데이터에 'game_pk' 컬럼이 없습니다. 실제 컬럼: {list(df.columns)}")
        return pd.DataFrame()

    # 2. JSON 정제
    for col in df.columns:
        sample = df[col].dropna()
        if not sample.empty and isinstance(sample.iloc[0], str) and sample.iloc[0].startswith('{'):
            try:
                expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else {})
                expanded_df = pd.json_normalize(expanded)
                expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
                df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
            except:
                continue
            
    # 3. 파이프라인 적용
    df = set_time_index(df)
    df = normalize_text_data(df)
    df = handle_missing_values(df)
    df = remove_outliers(df)
    df = optimize_data_types(df)
    df = add_matchup_stats(df)
    
    # 4. 레지스트리 생성
    if analysis_mode == "독립적":
        registry = pd.concat([create_main_registry(group) for _, group in df.groupby('game_year')])
    else:
        registry = create_main_registry(df)
    
    registry = add_rolling_features(registry)
    
    return registry
