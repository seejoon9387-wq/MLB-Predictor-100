import streamlit as st
from modules.data_loader import load_data
from modules.check_columns import show_column_names # 확인 모듈 불러오기

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    try:
        df = load_data()
        st.success("데이터 로드 성공!")
        
        # 1. 컬럼 확인 기능 호출
        show_column_names(df)
        
        # 2. 데이터 미리보기
        st.dataframe(df.head(100), use_container_width=True)
        
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
