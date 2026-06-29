import streamlit as st
from modules.data_loader import load_data

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 분석 엔진 (최신 데이터 모드)")
    
    try:
        registry = load_data()
        
        st.success("최신 데이터 로드 및 과거 기록 아카이빙 완료!")
        st.write(f"현재 엔진에서 분석 중인 경기 수: {len(registry)}")
        
        st.dataframe(registry.head(20), use_container_width=True)
        
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
