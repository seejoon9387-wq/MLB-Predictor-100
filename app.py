import streamlit as st
import pandas as pd
import ast
import gdown
import os

# 설정
FILE_ID = "1vj_n2MOPjAQ50U4N5KAxKxwuoL3UCaI4"
OUTPUT_FILE = "mlb_full_data.csv"

@st.cache_data
def load_large_data():
    # 1. 파일이 없으면 다운로드
    if not os.path.exists(OUTPUT_FILE):
        url = f'https://drive.google.com/uc?id={FILE_ID}'
        gdown.download(url, OUTPUT_FILE, quiet=False)
    
    # 2. 전체를 다 읽지 않고 필요한 부분만 처리 (메모리 최적화)
    # 데이터를 10만 행씩 나누어 읽어서 처리
    chunks = pd.read_csv(OUTPUT_FILE, chunksize=100000)
    df = pd.concat([c for c in chunks], ignore_index=True)
    
    # 3. 데이터 정제
    for col in df.columns:
        if isinstance(df[col].iloc[0], str) and df[col].iloc[0].startswith('{'):
            expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            expanded_df = pd.json_normalize(expanded)
            expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
            df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
    return df

def main():
    st.title("⚾ MLB 분석 엔진 (최적화 모드)")
    
    try:
        # 데이터 로드
        df = load_large_data()
        st.success("데이터 로드 성공!")
        st.dataframe(df.head(100)) # 100행만 보여주기
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")

if __name__ == "__main__":
    main()
