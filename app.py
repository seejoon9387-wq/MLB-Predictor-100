import streamlit as st
import pandas as pd
import ast
import os
import zipfile

# 1. 파일 설정 (zip 파일명 사용)
FILE_NAME = "mlb_full_data_slim.zip"

@st.cache_data
def load_data():
    # 2. ZIP 파일 처리
    if not os.path.exists(FILE_NAME):
        raise FileNotFoundError(f"{FILE_NAME} 파일을 찾을 수 없습니다. 깃허브 업로드 상태를 확인하세요.")
    
    # ZIP 파일 안의 첫 번째 CSV 파일을 읽음
    with zipfile.ZipFile(FILE_NAME, 'r') as z:
        file_list = z.namelist()
        with z.open(file_list[0]) as f:
            df = pd.read_csv(f)
    
    # 3. JSON 정제
    for col in df.columns:
        sample = df[col].dropna()
        if not sample.empty and isinstance(sample.iloc[0], str) and sample.iloc[0].startswith('{'):
            expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else {})
            expanded_df = pd.json_normalize(expanded)
            expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
            df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
    return df

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    try:
        df = load_data()
        st.success("데이터 로드 성공!")
        st.dataframe(df.head(100), use_container_width=True)
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
