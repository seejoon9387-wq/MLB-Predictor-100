import streamlit as st
import pandas as pd
import ast

# 데이터 로딩 및 정제 (메모리 최적화 포함)
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    
    # JSON처럼 생긴 문자열 컬럼을 자동으로 찾아서 펼치기
    for col in df.columns:
        # 데이터 샘플 체크: 문자열이고 '{'로 시작하는지 확인
        sample = df[col].dropna()
        if not sample.empty and isinstance(sample.iloc[0], str) and sample.iloc[0].startswith('{'):
            # 문자열을 파이썬 딕셔너리로 변환
            expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else {})
            # 딕셔너리 키를 새로운 컬럼으로 확장
            expanded_df = pd.json_normalize(expanded)
            expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
            # 원본 컬럼 삭제 및 확장 컬럼 병합
            df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
    return df

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    # 깃허브의 가벼운 파일 경로
    file_path = "mlb_full_data_slim.csv"
    
    try:
        df = load_data(file_path)
        st.success("데이터 로드 및 정제 완료!")
        
        # 이제 'team_id', 'team_name' 등으로 컬럼이 분리되어 나옵니다.
        st.dataframe(df.head(50), use_container_width=True)
        
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
