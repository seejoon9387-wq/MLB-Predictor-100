import streamlit as st
import pandas as pd
import json

FILE_PATHS = {
    "batters": "batters.csv.csv",
    "pitchers": "pitchers.csv.csv",
    "schedule": "schedule.csv.csv"
}

@st.cache_data
def load_data(file_path):
    data_list = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                # 각 줄이 JSON 객체 형태라면 파싱
                if line.startswith('{'):
                    data_list.append(json.loads(line))
            except json.JSONDecodeError:
                # 오류가 발생하면 무시하고 다음 줄로 이동
                continue
    
    # 딕셔너리 리스트를 데이터프레임으로 변환
    if data_list:
        return pd.DataFrame(data_list)
    return pd.DataFrame()

def main():
    st.set_page_config(page_title="MLB 분석 엔진", layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    all_data = {}
    for key, path in FILE_PATHS.items():
        try:
            all_data[key] = load_data(path)
        except Exception as e:
            st.error(f"파일 로딩 중 심각한 오류 ({key}): {e}")
    
    st.sidebar.title("메뉴")
    menu = st.sidebar.radio("분석 선택", ["데이터 요약", "선수 검색"])
    
    if menu == "데이터 요약":
        for name, df in all_data.items():
            if not df.empty:
                st.write(f"### {name} 데이터")
                st.dataframe(df, use_container_width=True)
            else:
                st.write(f"### {name} 데이터가 비어있거나 읽을 수 없습니다.")
    
    elif menu == "선수 검색":
        # ... (검색 로직) ...
        st.write("선수 검색 기능을 사용하려면 데이터가 성공적으로 로드되어야 합니다.")

if __name__ == "__main__":
    main()
