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

def load_data(source, is_url=False):
    if is_url:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(source, headers=headers)
        df = pd.read_csv(io.StringIO(response.text))
    else:
        df = pd.read_csv(source)
    
    # JSON 문자열 컬럼 처리
    for col in df.columns:
        # 데이터 샘플링을 통한 체크
        sample = df[col].dropna()
        if not sample.empty and isinstance(sample.iloc[0], str) and sample.iloc[0].startswith('{'):
            expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            expanded_df = pd.json_normalize(expanded)
            expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
            df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
    return df

def main():
    st.title("⚾ MLB 분석 엔진 디버깅")
    
    all_data = {}
    
    # 1. 로딩 단계별 추적
    try:
        st.write("로딩 시작...")
        
        for key, path in FILE_PATHS.items():
            st.write(f"{key} 로딩 중...")
            all_data[key] = load_data(path)
            
        st.write("구글 드라이브 데이터 로딩 중...")
        all_data["full_data"] = load_data(GOOGLE_DRIVE_URL, is_url=True)
        
        st.success("모든 데이터 로딩 완료!")
        st.dataframe(all_data["full_data"].head())
        
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")
        st.exception(e) # 오류의 원인을 상세히 표시

if __name__ == "__main__":
    main()
