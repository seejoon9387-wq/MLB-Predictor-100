import os
import subprocess
import sys

# 1. 라이브러리 자동 설치 및 체크 로직
def install_requirements():
    packages = ["pybaseball", "pytz"]
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_requirements()

# 2. 필수 라이브러리 임포트
import streamlit as st
import pandas as pd
from datetime import datetime
import pybaseball
import pytz
import re
import traceback

# 모듈 로드 방어
try:
    from modules.main_trainer import MLBUnifiedTrainer
except:
    MLBUnifiedTrainer = None

st.set_page_config(page_title="MLB Live Intelligence", layout="wide")

@st.cache_data(ttl=3600)
def get_live_schedule():
    # 올해 연도 설정
    year = datetime.now().year
    
    # 데이터 로드 (에러 시 빈 데이터프레임 반환)
    try:
        df = pybaseball.schedule_and_record(year, 'LAD')
        df = df.reset_index()
    except Exception as e:
        raise Exception(f"pybaseball 데이터 로드 실패: {e}")
    
    # 날짜 데이터 파싱 (강력한 정제)
    # mixed 모드로 다양한 형식 자동 감지
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    
    # 한국 시간(KST) 설정 및 변환
    kst = pytz.timezone('Asia/Seoul')
    df['Date'] = df['Date'].dt.tz_localize(None).dt.tz_localize('UTC').dt.tz_convert(kst)
    
    # Home/Away 팀 구분
    df['Away'] = df.apply(lambda x: x['Tm'] if x['Home_Away'] == '@' else x['Opp'], axis=1)
    df['Home'] = df.apply(lambda x: x['Opp'] if x['Home_Away'] == '@' else x['Tm'], axis=1)
    
    # 오늘 이후 경기만 필터링 (KST 기준)
    today = datetime.now(kst).replace(tzinfo=None)
    df = df[df['Date'].dt.tz_localize(None) >= today].sort_values(by='Date').reset_index(drop=True)
    
    # 표시용 데이터 생성
    df['Display_Date'] = df['Date'].dt.strftime('%m-%d (%a)')
    
    return df[['Date', 'Display_Date', 'Away', 'Home']]

def main():
    st.title("⚾ MLB 실시간 AI 분석 대시보드")
    
    try:
        with st.spinner("경기 데이터를 분석 중입니다..."):
            df = get_live_schedule()
            
        if df.empty:
            st.warning("예정된 경기가 없습니다.")
            return

        st.subheader("📅 오늘의 경기 및 향후 일정")
        
        event = st.dataframe(
            df[['Display_Date', 'Away', 'Home']], 
            use_container_width=True,
            hide_index=True,
            selection_mode="single-row",
            on_select="rerun"
        )
        
        if event.selection.rows:
            idx = event.selection.rows[0]
            selected_game = df.iloc[idx]
            
            st.divider()
            st.write(f"### 🔍 분석 대상: {selected_game['Away']} vs {selected_game['Home']} ({selected_game['Display_Date']})")
            
            if st.button("🚀 엔진 가동"):
                st.info("데이터 분석 엔진을 가동합니다...")
                
    except Exception as e:
        st.error("데이터 처리 중 오류가 발생했습니다.")
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
