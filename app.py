import streamlit as st
import pandas as pd
from modules import summary, search

# 깃허브에 올린 파일명과 정확히 일치하게 입력하세요 (대소문자 주의!)
FILE_PATHS = {
    "batters": "batters.csv",
    "pitchers": "pitchers.csv",
    "full_data": "full_data.csv",
    "schedule": "schedule.csv"
}

@st.cache_data
def load_all_data():
    data = {}
    errors = []
    for key, file_path in FILE_PATHS.items():
        try:
            # 깃허브 경로에 있는 파일을 직접 읽음
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
