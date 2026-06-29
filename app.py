# app.py
import streamlit as st
from modules.data_loader import load_data

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    try:
        # 모듈에서 가져온 데이터 로딩 함수 사용
        df = load_data()
        st.success("데이터 로드 성공!")
        
        # 데이터 시각화
        st.dataframe(df.head(100), use_container_width=True)
        
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
