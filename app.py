import streamlit as st
import pandas as pd
import json

# 파일 경로 정의 (존재하는 파일만 적었습니다)
FILE_PATHS = {
    "batters": "batters.csv.csv",
    "pitchers": "pitchers.csv.csv",
    "schedule": "schedule.csv.csv"
}

@st.cache_data
def load_and_parse(file_path):
    # 1. 파일 전체를 텍스트로 읽기
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # 2. 내용이 '{'로 시작하면 JSONL(한 줄씩 JSON)로 간주하고 변환
    if content.startswith('{'):
        data_list = [json.loads(line) for line in content.split('\n') if line.strip()]
        return pd.json_normalize(data_list)
    # 3. 아니면 CSV로 읽기
    else:
        from io import StringIO
        return pd.read_csv(StringIO(content))

def main():
    st.set_page_config(page_title="MLB 분석 엔진", layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    data = {}
    for key, path in FILE_PATHS.items():
        try:
            data[key] = load_and_parse(path)
        except Exception as e:
            st.error(f"로딩 실패 ({key}): {e}")
    
    if not data:
        st.stop()
        
    st.sidebar.title("메뉴")
    menu = st.sidebar.radio("분석 선택", ["데이터 요약", "선수 검색"])
    
    if menu == "데이터 요약":
        # summary.show(data) 부분을 직접 구현 (파일 불러오기 문제 해결 확인용)
        for name, df in data.items():
            st.write(f"### 데이터: {name}")
            st.dataframe(df.head(10))
    elif menu == "선수 검색":
        # search.show(data)
        st.write("선수 검색 기능을 사용하려면 summary가 먼저 성공해야 합니다.")

if __name__ == "__main__":
    main()
