import streamlit as st
from modules.data_loader import load_data

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    try:
        df = load_data()
        
        st.success("데이터 로드 및 최적화 완료!")
        
        # 메모리 사용량 확인 (MB 단위)
        mem_usage = df.memory_usage(deep=True).sum() / 1024**2
        st.write(f"현재 데이터프레임 메모리 점유율: {mem_usage:.2f} MB")
        
        st.dataframe(df.head(100), use_container_width=True)
        
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
