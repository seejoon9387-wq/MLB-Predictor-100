import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="MLB Status", layout="wide")

def main():
    st.title("⚾ MLB 시스템 복구 모드")
    
    # 1. API 호출 테스트
    try:
        url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=2026-06-29&endDate=2026-06-29"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        st.success("데이터 통신 성공!")
        st.write("데이터 수신 완료.")
        
        # 2. 데이터 구조 확인 (디버깅용)
        st.write(data)
        
    except Exception as e:
        st.error(f"코드 실행 중 에러 발생: {e}")

if __name__ == "__main__":
    main()
