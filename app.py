import streamlit as st
import pandas as pd
import requests
import io

st.title("데이터 컬럼명 탐색기")

FILE_ID = "1iSbcXGYzInvd5LQ1jLqdq0MgMtTT09pw"
DATA_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

@st.cache_data
def get_csv_columns(url):
    # 첫 100줄만 읽어서 구조를 파악 (메모리 절약)
    response = requests.get(url)
    df = pd.read_csv(io.BytesIO(response.content), nrows=100)
    return df.columns.tolist()

try:
    cols = get_csv_columns(DATA_URL)
    st.write("### CSV 파일에 들어있는 실제 컬럼명들입니다:")
    st.write(cols)
    st.write("---")
    st.write("위 목록에서 필요한 컬럼명을 복사해서 저에게 알려주세요!")
except Exception as e:
    st.error(f"오류 발생: {e}")
