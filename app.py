import streamlit as st
import pandas as pd
import ast
import requests
import io

FILE_PATHS = {
    "batters": "batters.csv.csv",
    "pitchers": "pitchers.csv.csv",
    "schedule": "schedule.csv.csv"
}

GOOGLE_DRIVE_URL = "https://drive.google.com/uc?export=download&id=1vj_n2MOPjAQ50U4N5KAxKxwuoL3UCaI4"

@st.cache_data
def load_data(source, is_url=False):
    if is_url:
        # 구글 드라이브 접속 시도
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(source, headers=headers)
        if response.status_code != 200:
            raise Exception(f"구글 드라이브 서버 응답 오류: {response.status_code}")
        df = pd.read_csv(io.StringIO(response.text))
    else:
        df = pd.read_csv(source)
    
    # 데이터가 비어있는지 확인
    if df.empty:
        raise Exception("파일은 로드되었으나 데이터가 비어있습니다.")
        
    # JSON 문자열 컬럼 처리 (첫 번째 줄이 비어있을 경우 대비)
    for col in df.columns:
        # 데이터가 있고, 첫 번째 값이 문자열이며 '{'로 시작할 때만 동작
        if not df[col].dropna().empty and isinstance(df[col].dropna().iloc[0], str) and df[col].dropna().iloc[0].startswith('{'):
            expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            expanded_df = pd.json_normalize(expanded)
            expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
            df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
    return df

# ... main 함수 생략 (위와 동일)
