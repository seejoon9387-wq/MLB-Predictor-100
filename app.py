import streamlit as st
import pandas as pd

# 구글 드라이브 파일 ID
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
            # 구글 드라이브 직접 다운로드 URL 생성
            url = f"https://drive.google.com/uc?export=download&id={file_id}"
            df = pd.read_csv(url)
            data[key] = df
        except Exception as e:
            errors.append(f"로딩 실패 ({key}): {str(e)}")
            
    return data, errors

def main():
    st.set_page_config(page_title="MLB 분석 엔진", layout="wide")
    st.title("⚾ MLB 분석 엔진 v1.0.1")
    
    with st.spinner('데이터를 엔진에 연동 중입니다...'):
        data, errors = load_all_data()
    
    if errors:
        for err in errors:
            st.error(err)
        st.stop()
        
    st.success("데이터 연동 완료!")
    st.write("분석을 시작할 준비가 되었습니다.")

if __name__ == "__main__":
    main()
