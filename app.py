import streamlit as st
import pandas as pd
import ast

# 깃허브에 있는 파일들만 사용 (구글 드라이브 연결 제거)
FILE_PATHS = {
    "batters": "batters.csv.csv",
    "pitchers": "pitchers.csv.csv",
    "full_data": "full_data_small.csv" # 20MB 이하로 줄인 파일명
}

@st.cache_data
def load_data(file_path):
    # 파일이 존재하는지 먼저 확인
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        return None
    
    # JSON 문자열 컬럼 처리 (이미 수행한 로직)
    for col in df.columns:
        sample = df[col].dropna()
        if not sample.empty and isinstance(sample.iloc[0], str) and sample.iloc[0].startswith('{'):
            expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            expanded_df = pd.json_normalize(expanded)
            expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
            df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
    return df

def main():
    st.set_page_config(page_title="MLB 분석 엔진", layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    all_data = {}
    
    for key, path in FILE_PATHS.items():
        data = load_data(path)
        if data is not None:
            all_data[key] = data
            
    if not all_data:
        st.error("데이터 파일을 찾을 수 없습니다. 깃허브 폴더를 확인하세요.")
        return

    menu = st.sidebar.radio("분석 선택", ["데이터 요약", "선수 검색"])
    dataset = st.selectbox("데이터셋 선택", list(all_data.keys()))
    
    if menu == "데이터 요약":
        st.dataframe(all_data[dataset].head(500), use_container_width=True)
    elif menu == "선수 검색":
        query = st.text_input("검색어 입력")
        if query:
            df = all_data[dataset]
            mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
            st.dataframe(df[mask], use_container_width=True)

if __name__ == "__main__":
    main()
