import streamlit as st
import pandas as pd
import requests
import json
import io
from modules import summary, search

FILE_IDS = {
    "batters": "1UAgU7QH65LOqAaicg-Snrn26wfniDOWT",
    "pitchers": "1jNHpBgB_NXuI5Aedw5j0qG05u9eSFyHT",
    "full_data": "1vj_n2MOPjAQ50U4N5KAxKxwuoL3UCaI4",
    "schedule": "1jNvhwD_1nQhW9pnyVodutjtZfY03b4-Q"
}

@st.cache_data
def load_all_data():
    data = {}
    errors = []
    for key, file_id in FILE_IDS.items():
        try:
            url = f"https://drive.google.com/uc?export=download&id={file_id}"
            response = requests.get(url)
            
            # 1. 데이터를 줄 단위로 JSON 리스트로 읽기
            lines = [json.loads(line) for line in response.text.strip().split('\n') if line.strip()]
            
            # 2. json_normalize를 사용하여 딕셔너리 키를 컬럼으로 펼치기
            df = pd.json_normalize(lines)
            
            data[key] = df
        except Exception as e:
            errors.append(f"로딩 실패 ({key}): {str(e)}")
    return data, errors

def main():
    st.set_page_config(page_title="MLB 분석 엔진", layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    data, errors = load_all_data()
    
    if errors:
        for err in errors: st.error(err)
        st.stop()
        
    st.sidebar.title("메뉴")
    menu = st.sidebar.radio("분석 선택", ["데이터 요약", "선수 검색"])
    
    if menu == "데이터 요약": summary.show(data)
    elif menu == "선수 검색": search.show(data)

if __name__ == "__main__":
    main()
