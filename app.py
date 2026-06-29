import streamlit as st
from modules.data_loader import load_data

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 분석 엔진: 통합 경기 레지스트리")
    
    try:
        # 데이터 로드 (registry 테이블)
        registry = load_data()
        
        st.success("경기 중심 통합 테이블 생성 완료!")
        st.write(f"총 {len(registry)}개의 경기가 등록되었습니다.")
        
        # 경기 데이터 미리보기
        st.dataframe(registry.head(20), use_container_width=True)
        
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
