import streamlit as st
import pandas as pd
from modules import summary, search

# 깃허브 파일 목록에 실제 존재하는 파일명만 남겼습니다.
FILE_PATHS = {
    "batters": "batters.csv.csv",
    "pitchers": "pitchers.csv.csv",
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
        # 로딩 실패가 발생해도 존재하는 파일들로 실행 가능하게 합니다.
    
    st.sidebar.title("메뉴")
    menu = st.sidebar.radio("분석 선택", ["데이터 요약", "선수 검색"])
    
    if menu == "데이터 요약":
        summary.show(data)
    elif menu == "선수 검색":
        search.show(data)

if __name__ == "__main__":
    main()
