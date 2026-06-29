import streamlit as st
import pandas as pd
import ast
import requests
import io

# 1. 설정
FILE_PATHS = {
    "batters": "batters.csv.csv",
    "pitchers": "pitchers.csv.csv",
    "schedule": "schedule.csv.csv"
}
GOOGLE_DRIVE_URL = "https://drive.google.com/uc?export=download&id=1vj_n2MOPjAQ50U4N5KAxKxwuoL3UCaI4"

# 2. 데이터 로드 함수 (오류 방지 로직 포함)
@st.cache_data
def load_data(source, is_url=False):
    if is_url:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(source, headers=headers)
        # 구글 드라이브가 로그인 페이지(HTML)를 주는지 확인
        if "text/html" in response.headers.get("Content-Type", ""):
            raise Exception("구글 드라이브 접근 오류: 파일 공유 설정이 '링크가 있는 모든 사용자'인지 확인하세요.")
        df = pd.read_csv(io.StringIO(response.text))
    else:
        df = pd.read_csv(source)
    
    # 딕셔너리 형태의 문자열을 컬럼으로 펼치기
    for col in df.columns:
        sample = df[col].dropna()
        if not sample.empty and isinstance(sample.iloc[0], str) and sample.iloc[0].startswith('{'):
            expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            expanded_df = pd.json_normalize(expanded)
            expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
            df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
    return df

# 3. 메인 화면
def main():
    st.set_page_config(page_title="MLB 분석 엔진", layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    all_data = {}
    
    # 데이터 로드
    try:
        # 깃허브 데이터
        for key, path in FILE_PATHS.items():
            all_data[key] = load_data(path)
        
        # 구글 드라이브 데이터
        all_data["full_data"] = load_data(GOOGLE_DRIVE_URL, is_url=True)
        
        st.success("모든 데이터 로딩 성공!")
        
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
