import streamlit as st
from modules.data_loader import load_data
from modules.check_columns import show_column_names

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    try:
        # 데이터 로드 및 전처리 파이프라인 실행
        df = load_data()
        
        # 처리 결과 확인
        st.success("데이터 로드 및 결측치 처리 완료!")
        
        # 결측치가 남아있는지 마지막으로 확인 (디버깅)
        missing_count = df.isnull().sum().sum()
        if missing_count == 0:
            st.info("현재 데이터셋에 결측치가 없습니다.")
        else:
            st.warning(f"경고: 처리되지 않은 결측치가 {missing_count}개 남아있습니다.")
        
        show_column_names(df)
        st.dataframe(df.head(100), use_container_width=True)
        
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
