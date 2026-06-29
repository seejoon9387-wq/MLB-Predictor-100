import streamlit as st
from modules.data_loader import load_data
from modules.check_columns import show_column_names

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    try:
        # 데이터 로드 및 시계열 정렬
        df = load_data()
        st.success("데이터 로드 및 시계열 인덱싱 완료!")
        
        # 컬럼 확인 및 데이터 미리보기
        show_column_names(df)
        st.dataframe(df.head(100), use_container_width=True)
        
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
