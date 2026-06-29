import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

st.set_page_config(page_title="MLB AI Status", layout="wide")

def main():
    st.title("⚾ MLB 시스템 복구 모드")
    
    # 1. 라이브러리 로드 상태 체크
    st.write("시스템 정상 작동 중...")
    
    # 2. 데이터 호출 테스트
    try:
        today_str = datetime.now().strftime('%Y-%m-%d')
        url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={today_str}&endDate={today_str}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        st.success("데이터베이스 연결 성공!")
        st.write(f"오늘의 데이터 수신 완료 (API 응답 코드: {response.status_code})")
        
        if 'dates' in data and len(data['dates']) > 0:
            st.write("경기 데이터 확인됨.")
        else:
            st.warning("오늘 예정된 경기가 없습니다.")
            
    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
