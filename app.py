import streamlit as st
import pandas as pd
from datetime import datetime
import pybaseball

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    year = datetime.now().year
    # LAD 팀 데이터를 기준으로 샘플 로드
    data = pybaseball.schedule_and_record(year, 'LAD')
    return data

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
    try:
        df = get_live_schedule()
        
        # 1. 여기서 컬럼 목록을 확인합니다.
        st.write("### 현재 데이터의 컬럼 목록:")
        st.write(df.columns.tolist())
        
        st.subheader("📅 경기 일정 (데이터 확인용)")
        st.dataframe(df.head(), use_container_width=True)
        
        # 데이터가 정상적으로 들어오면 아래 로직을 통해 실제 경기 매칭
        # 사용 가능한 컬럼명을 알려주시면 바로 아래 코드를 완성해 드릴게요.
        
    except Exception as e:
        st.error(f"오류 발생: {e}")
        st.write("위의 '현재 데이터의 컬럼 목록' 리스트를 저에게 복사해서 알려주세요!")

if __name__ == "__main__":
    main()
