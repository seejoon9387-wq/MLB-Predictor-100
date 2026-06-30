import streamlit as st
import pandas as pd
import requests
import io

st.title("컬럼명 확인 도구")

FILE_ID = "1iSbcXGYzInvd5LQ1jLqdq0MgMtTT09pw"
DATA_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

@st.cache_data
def get_columns(url):
    response = requests.get(url)
    df_preview = pd.read_csv(io.BytesIO(response.content), nrows=5)
    return df_preview.columns.tolist()

try:
    cols = get_columns(DATA_URL)
    st.write("### 현재 CSV에 있는 컬럼명들:")
    st.write(cols)
except Exception as e:
    st.error(f"오류 발생: {e}")
