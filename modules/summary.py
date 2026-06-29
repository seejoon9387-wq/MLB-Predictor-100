import streamlit as st

def show(data):
    st.subheader("데이터 요약 모듈")
    for name, df in data.items():
        st.write(f"### [데이터셋: {name}]")
        st.dataframe(df.head(20), use_container_width=True)
