import streamlit as st
import pandas as pd
from modules import summary, search

# 웹에 게시된 CSV 링크를 여기에 넣으세요
CSV_URLS = {
    "batters": "여기에_배터_CSV_링크_붙여넣기",
    "pitchers": "여기에_투수_CSV_링크_붙여넣기",
    "full_data": "여기에_풀데이터_CSV_링크_붙여넣기",
    "schedule": "여기에_일정_CSV_링크_붙여넣기"
}

@st.cache_data
def load_all_data():
    data = {}
    errors = []
    for key, url in CSV_URLS.items():
        try:
            # CSV를 직접 읽습니다. 
            data[key] = pd.read_csv(url)
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
    if menu == "데이터 요약": summary.show(data)
    elif menu == "선수 검색": search.show(data)

if __name__ == "__main__":
    main()
