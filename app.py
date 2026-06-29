import streamlit as st
import pandas as pd
import json
import io

# 깃허브에 있는 파일명들
FILE_PATHS = {
    "batters": "batters.csv.csv",
    "pitchers": "pitchers.csv.csv",
    "schedule": "schedule.csv.csv"
}

@st.cache_data
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 1. 파일 내용이 { 로 시작하는지 확인 (JSON 형식인지 체크)
    if lines[0].strip().startswith('{'):
        # JSONL 데이터를 딕셔너리 리스트로 변환
        data_list = [json.loads(line) for line in lines if line.strip()]
        return pd.DataFrame(data_list)
    else:
        # 일반 CSV인 경우
        return pd.read_csv(io.StringIO("".join(lines)))

def main():
    st.set_page_config(page_title="MLB 분석 엔진", layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    all_data = {}
    for key, path in FILE_PATHS.items():
        try:
            all_data[key] = load_data(path)
        except Exception as e:
            st.error(f"파일 로딩 오류 ({key}): {e}")
    
    if not all_data:
        st.stop()

    st.sidebar.title("메뉴")
    menu = st.sidebar.radio("분석 선택", ["데이터 요약", "선수 검색"])
    
    if menu == "데이터 요약":
        for name, df in all_data.items():
            st.write(f"### {name} 데이터")
            st.dataframe(df, use_container_width=True)
            
    elif menu == "선수 검색":
        dataset = st.selectbox("데이터셋 선택", list(all_data.keys()))
        df = all_data[dataset]
        query = st.text_input("검색어 입력")
        if query:
            mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
            st.dataframe(df[mask], use_container_width=True)

if __name__ == "__main__":
    main()
