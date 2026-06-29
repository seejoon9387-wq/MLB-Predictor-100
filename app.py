import streamlit as st
import pandas as pd
import ast
import os

# 깃허브에 올린 파일명 사용 (직접 다운로드 안 함!)
# 파일이 크다면 엑셀에서 미리 2026년 데이터만 필터링해서 저장하세요.
DATA_FILE = "full_data.csv" 

@st.cache_data
def load_and_process_data():
    if not os.path.exists(DATA_FILE):
        return None
    
    # 1. 원본을 다 읽지 않고 필요한 컬럼만 지정해서 읽기 (메모리 절약)
    # 필요한 컬럼이 무엇인지 명시하면 훨씬 빨라집니다.
    df = pd.read_csv(DATA_FILE, nrows=50000) # 일단 5만 행만 읽기
    
    # 2. JSON 컬럼 처리 (메모리 튀지 않게 한 컬럼씩 순차 처리)
    for col in df.columns:
        if df[col].dtype == 'object' and df[col].astype(str).str.startswith('{').any():
            expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else {})
            expanded_df = pd.json_normalize(expanded)
            df = df.drop(columns=[col]).join(expanded_df)
    return df

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 분석 엔진 (초경량 모드)")
    
    df = load_and_process_data()
    
    if df is None:
        st.error(f"파일({DATA_FILE})을 찾을 수 없습니다. 깃허브에 파일을 업로드했는지 확인하세요.")
        return

    st.success("데이터 로드 완료! (최적화 모드)")
    
    # 검색 기능
    query = st.text_input("선수 이름 검색:")
    if query:
        mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
        st.dataframe(df[mask])
    else:
        st.dataframe(df.head(100))

if __name__ == "__main__":
    main()
