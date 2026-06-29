import streamlit as st

def show(data):
    st.subheader("데이터 요약 모듈")
    for name, df in data.items():
        st.write(f"### {name}")
        st.write(df.head())
