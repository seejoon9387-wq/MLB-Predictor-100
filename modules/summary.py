import streamlit as st
import pandas as pd

def show(data):
    st.subheader("데이터 요약 모듈")
    # 여기서 각 데이터프레임의 상태를 보여주는 로직 작성
    for name, df in data.items():
        st.write(f"### {name}")
        st.dataframe(df.head())
