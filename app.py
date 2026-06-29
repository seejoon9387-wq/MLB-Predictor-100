import streamlit as st
import pandas as pd
import ast
import gdown
import os

FILE_PATHS = {
    "batters": "batters.csv.csv",
    "pitchers": "pitchers.csv.csv",
    "schedule": "schedule.csv.csv"
}

# 구글 드라이브 파일 ID만 사용합니다.
FILE_ID = "1vj_n2MOPjAQ50U4N5KAxKxwuoL3UCaI4"
OUTPUT_FILE = "mlb_full_data.csv"

@st.cache_data
def load_data(source, is_google_drive=False):
    if is_google_drive:
        # 파일이 로컬에 없으면 다운로드
        if not os.path.exists(OUTPUT_FILE):
            url = f'https://drive.google.com/uc?id={source}'
            gdown.download(url, OUTPUT_FILE, quiet=False)
        df = pd.read_csv(OUTPUT_FILE)
    else:
        df = pd.read_csv(source)
    
    # JSON 문자열 컬럼 펼치기
    for col in df.columns:
        sample = df[col].dropna()
        if not sample.empty and isinstance(sample.iloc[0], str) and sample.iloc[0].startswith('{'):
            expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            expanded_df = pd.json_normalize(expanded)
            expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
            df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
    return df

def main():
    st.set_page_config(page_title="⚾ MLB 분석 엔진", layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    all_data = {}
    
    try:
        # 깃허브 파일 로드
        for key, path in FILE_PATHS.items():
            all_data[key] = load_data(path)
        
        # 구글 드라이브 파일 로드
        with st.spinner('구글 드라이브 데이터를 불러오는 중...'):
            all_data["full_data"] = load_data(FILE_ID, is_google_drive=True)
            
        st.success("데이터 로딩 완료!")
        
        # 메뉴
        menu = st.sidebar.radio("분석 선택", ["데이터 요약", "선수 검색"])
        dataset = st.selectbox("데이터셋 선택", list(all_data.keys()))
        
        if menu == "데이터 요약":
            st.dataframe(all_data[dataset], use_container_width=True)
        elif menu == "선수 검색":
            query = st.text_input("검색어 입력")
            if query:
                df = all_data[dataset]
                mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
                st.dataframe(df[mask], use_container_width=True)
                
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
