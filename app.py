import streamlit as st
import pandas as pd
import requests
import io

st.title("MLB 데이터 로더 (Direct Mode)")

# 구글 드라이브 파일 ID
FILE_ID = "1iSbcXGYzInvd5LQ1jLqdq0MgMtTT09pw"
# 강제 다운로드 URL 형식
DATA_URL = f"https://drive.usercontent.google.com/download?id={FILE_ID}&export=download&confirm=t"

@st.cache_data
def load_data(url):
    # 헤더를 추가하여 브라우저처럼 인식하게 함
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return pd.read_csv(io.BytesIO(response.content), nrows=100) # 일단 100줄만 읽어보자
    else:
        raise Exception(f"다운로드 실패. 상태 코드: {response.status_code}")

try:
    cols = load_data(DATA_URL).columns.tolist()
    st.write("### 드디어 실제 컬럼명을 확인했습니다:")
    st.write(cols)
except Exception as e:
    st.error(f"오류 발생: {e}")
