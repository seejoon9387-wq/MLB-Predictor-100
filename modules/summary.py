import streamlit as st
import pandas as pd

def show(data):
    st.subheader("데이터 요약 모듈")
    st.info("데이터프레임의 제목을 클릭하면 상세 표가 펼쳐집니다.")
    
    for name, df in data.items():
        st.write(f"### [데이터셋: {name}]")
        
        # 데이터가 비어있는지 확인
        if df is None or df.empty:
            st.warning(f"{name} 데이터가 비어있습니다.")
            continue
            
        # 데이터프레임 확인 (디버깅용)
        st.write(f"행: {len(df)}개, 열: {len(df.columns)}개")
        
        # 여기서 확실하게 대화형 표로 출력
        st.dataframe(df.head(20), use_container_width=True)
        
        # 만약 데이터가 너무 많아 복사가 안 될 경우를 대비해 다운로드 버튼 제공
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"{name} 전체 데이터 다운로드(CSV)",
            data=csv,
            file_name=f"{name}_data.csv",
            mime='text/csv'
        )
