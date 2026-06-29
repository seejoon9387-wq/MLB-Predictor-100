import streamlit as st
import pandas as pd
import ast

# 파일 경로
FILE_PATHS = {
    "batters": "batters.csv.csv" # 데이터가 들어있는 파일명으로 수정하세요
}

@st.cache_data
def load_data(file_path):
    # CSV를 읽되, 일단 모든 것을 문자열로 읽음
    df = pd.read_csv(file_path)
    
    # 딕셔너리처럼 보이는 문자열 컬럼들을 찾아 실제 딕셔너리로 변환 후 컬럼 분리
    for col in df.columns:
        # 첫 번째 값이 '{'로 시작하면 딕셔너리 형태의 문자열임
        if isinstance(df[col].iloc[0], str) and df[col].iloc[0].startswith('{'):
            # 문자열을 실제 딕셔너리로 변환
            expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            # 딕셔너리 내부 키(예: name, fullName)를 새로운 컬럼으로 생성
            expanded_df = pd.json_normalize(expanded)
            # 기존 컬럼 이름 뒤에 접미사 추가하여 병합 (예: team.name)
            expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
            df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
            
    return df

def main():
    st.set_page_config(page_title="MLB 분석 엔진", layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    try:
        df = load_data("batters.csv.csv")
        st.write("### 데이터 요약")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"데이터 로딩 실패: {e}")

if __name__ == "__main__":
    main()
