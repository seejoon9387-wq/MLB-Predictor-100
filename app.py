import streamlit as st
from modules.data_loader import load_data

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 분석 엔진: 시즌 분석 모드 설정")
    
    # 분석 모드 스위치
    mode = st.radio(
        "데이터 분석 모드를 선택하세요:",
        ("연속적", "독립적"),
        help="연속적: 전체 데이터를 통합 분석합니다. / 독립적: 시즌별로 데이터를 격리하여 분석합니다."
    )
    
    try:
        # 선택된 모드에 따라 데이터 로드
        registry = load_data(analysis_mode=mode)
        
        st.success(f"{mode} 모드로 데이터 로드 완료!")
        st.write(f"현재 분석 경기 수: {len(registry)}")
        
        st.dataframe(registry.head(20), use_container_width=True)
        
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
