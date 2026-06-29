import streamlit as st
from modules import summary, search  # modules 폴더에서 기능을 가져옴

# ... (기존 데이터 로드 load_all_data 함수는 여기에 유지) ...

def main():
    st.set_page_config(page_title="MLB 분석 엔진", layout="wide")
    data, errors = load_all_data() # 데이터 로드
    
    st.sidebar.title("메뉴")
    menu = st.sidebar.radio("분석 선택", ["데이터 요약", "선수 검색"])

    if menu == "데이터 요약":
        summary.show(data) # modules/summary.py 실행
    elif menu == "선수 검색":
        search.show(data)  # modules/search.py 실행

if __name__ == "__main__":
    main()
