import streamlit as st
import pandas as pd
import requests
import json
import io
from modules import summary, search

# 구글 드라이브 파일 ID (기존 ID 유지)
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
            # 핵심: 구글 드라이브 API를 통한 직접 파일 스트림 접근
            url = f"https://docs.google.com/uc?export=download&id={file_id}"
            response = requests.get(url)
            response.raise_for_status() # 오류 발생 시 즉시 감지
            
            # JSONL(줄바꿈 구분 JSON) 형식으로 읽기 시도
            lines = response.text.strip().split('\n')
            data_list = [json.loads(line) for line in lines if line.strip()]
            data[key] = pd.json_normalize(data_list)
            
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
