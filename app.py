import streamlit as st
from modules.data_loader import load_data

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 분석 엔진 (이상치 정화 모드)")
    
    try:
        registry = load_data()
        st.success("데이터 로드, 정화 및 최적화 완료!")
        st.write(f"현재 분석 가능한 경기 수: {len(registry)}")
        
        st.dataframe(registry.head(20), use_container_width=True)
        
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
