import streamlit as st

def show(data):
    st.subheader("데이터 요약 모듈")
    st.info("표의 셀을 클릭하거나 드래그하여 데이터를 복사할 수 있습니다.")
    
    for name, df in data.items():
        st.write(f"### {name}")
        # dataframe을 사용하면 사용자가 직접 복사/붙여넣기 가능
        st.dataframe(df.head(10), use_container_width=True)
