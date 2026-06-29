import streamlit as st
import pandas as pd
import ast
import requests
import io

# 깃허브 파일 목록
FILE_PATHS = {
    "batters": "batters.csv.csv",
    "pitchers": "pitchers.csv.csv",
    "schedule": "schedule.csv.csv"
}

# 구글 드라이브 링크
GOOGLE_DRIVE_URL = "https://drive.google.com/uc?export=download&id=1vj_n2MOPjAQ50U4N5KAxKxwuoL3UCaI4"

@st.cache_data
def load_data(source, is_url=False):
    """CSV 내 JSON 문자열을 처리하여 데이터프레임으로 변환하는 함수"""
    if is_url:
        response = requests.get(source)
        df = pd.read_csv(io.StringIO(response.text))
    else:
        df = pd.read_csv(source)
    
    # JSON 문자열 컬럼 처리
    for col in df.columns:
        if isinstance(df[col].iloc[0], str) and df[col].iloc[0].startswith('{'):
            expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            expanded_df = pd.json_normalize(expanded)
            expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
            df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
    return df

def main():
    st.set_page_config(page_title="⚾ MLB 분석 엔진", layout="wide")
    st.title("⚾ MLB 분석 엔진 (통합 버전)")
    
    all_data = {}
    
    # 1. 깃허브 파일 로드
    with st.spinner('깃허브 데이터를 불러오는 중...'):
        for key, path in FILE_PATHS.items():
            try:
                all_data[key] = load_data(path)
            except Exception as e:
                st.error(f"깃허브 데이터 로딩 실패 ({key}): {e}")
    
    # 2. 구글 드라이브 데이터 로드
    with st.spinner('구글 드라이브 데이터를 불러오는 중...'):
        try:
            all_data["full_data"] = load_data(GOOGLE_DRIVE_URL, is_url=True)
        except Exception as e:
            st.error(f"구글 드라이브 데이터 로딩 실패: {e}")
    
    # 메뉴 선택
    st.sidebar.title("메뉴")
    menu = st.sidebar.radio("분석 선택", ["데이터 요약", "선수 검색"])
    
    if menu == "데이터 요약":
        dataset = st.selectbox("데이터셋 선택", list(all_data.keys()))
        if dataset in all_data:
            st.write(f"### {dataset} 데이터 요약")
            st.dataframe(all_data[dataset], use_container_width=True)
            
    elif menu == "선수 검색":
        dataset = st.selectbox("데이터셋 선택", list(all_data.keys()))
        df = all_data[dataset]
        query = st.text_input("검색어를 입력하세요:")
        if query:
            mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
            st.dataframe(df[mask], use_container_width=True)

if __name__ == "__main__":
    main()
