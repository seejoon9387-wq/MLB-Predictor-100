import streamlit as st
import pandas as pd
import traceback

# 1. 초기 로드 단계에서 에러가 나면 화면에 표시
try:
    from datetime import datetime
    import pybaseball
    import pytz
    import re
    # 모듈 임포트 에러 방지
    try:
        from modules.main_trainer import MLBUnifiedTrainer
    except:
        MLBUnifiedTrainer = None
except Exception as e:
    st.error(f"라이브러리 로드 중 오류: {e}")
    st.stop()

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

def get_live_schedule():
    # 올해 연도 설정
    year = datetime.now().year
    # LAD 데이터 로드
    df = pybaseball.schedule_and_record(year, 'LAD')
    df = df.reset_index()
    
    # 날짜 파싱 방어 코드
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    
    # 시간대 처리
    kst = pytz.timezone('Asia/Seoul')
    df['Date'] = df['Date'].dt.tz_localize(None).dt.tz_localize('UTC').dt.tz_convert(kst)
    
    # 데이터 매핑
    df['Away'] = df.apply(lambda x: x['Tm'] if x['Home_Away'] == '@' else x['Opp'], axis=1)
    df['Home'] = df.apply(lambda x: x['Opp'] if x['Home_Away'] == '@' else x['Tm'], axis=1)
    
    # 정렬
    today = datetime.now(kst).replace(tzinfo=None)
    df = df[df['Date'].dt.tz_localize(None) >= today].sort_values(by='Date').reset_index(drop=True)
    df['Display_Date'] = df['Date'].dt.strftime('%m-%d (%a)')
    
    return df[['Date', 'Display_Date', 'Away', 'Home']]

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
    try:
        with st.spinner("데이터 로드 중..."):
            df = get_live_schedule()
            
        st.dataframe(df[['Display_Date', 'Away', 'Home']], use_container_width=True, hide_index=True)
        
    except Exception:
        # 에러 발생 시 구체적인 추적 정보를 화면에 출력
        st.error("앱 실행 중 오류가 발생했습니다. 아래 상세 내용을 확인하세요.")
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
