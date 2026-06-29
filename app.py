import streamlit as st
import pandas as pd
from modules import summary, search

# 깃허브에 업로드된 파일명과 정확히 일치시켰습니다 (.csv.csv 확인)
FILE_PATHS = {
    "batters": "batters.csv.csv",
    "pitchers": "pitchers.csv.csv",
    "full_data": "full_data.csv.csv",
    "schedule": "schedule.csv.csv"
}

@st.cache_data
def load_all_data():
    data = {}
    errors = []
    for key, file_path in FILE_PATHS.items():
        try:
            # 깃허브의 파일 경로를 읽어옵니다.
            data[key] = pd.read_csv(file_path)
        except Exception as e:
            errors.append(f"로딩 실패 ({key}): {str(e)}")
    return data, errors

def main():
    st.set_page_config(page_title="MLB 분석 엔진", layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    data, errors = load_all_data()
    if errors:
        for err in errors: st.error(err)
        st.stop()
        
    st.sidebar.title("메뉴")
    menu = st.sidebar.radio("분석 선택", ["데이터 요약", "선수 검색"])
    
    if menu == "데이터 요약":
        summary.show(data)
    elif menu == "선수 검색":
        search.show(data)

if __name__ == "__main__":
    main()
