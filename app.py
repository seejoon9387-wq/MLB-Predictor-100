import streamlit as st
import pandas as pd
import numpy as np
import os
from modules.data_manager import DataManager
from modules.ui_manager import UIManager

# --- 엔진 핵심부: 데이터 로드 및 예측 ---
def get_prediction(home_name, away_name):
    try:
        # 파일 로드 (압축 파일이므로 pd.read_csv에 바로 적용)
        batters = pd.read_csv('batters.csv.csv')
        pitchers = pd.read_csv('pitchers.csv.csv')
        
        # 홈/원정팀 데이터 추출 (팀명 컬럼이 'team'이라고 가정)
        home_pitchers = pitchers[pitchers['team'] == home_name]
        away_pitchers = pitchers[pitchers['team'] == away_name]
        
        # 간단한 예측 로직: ERA(평균자책점)가 낮은 팀이 유리
        # 0에 가까울수록 좋으므로 역수를 취함
        home_score = 1 / (home_pitchers['era'].mean() + 0.1)
        away_score = 1 / (away_pitchers['era'].mean() + 0.1)
        
        # 승률 계산 (로지스틱 함수)
        prob = 1 / (1 + np.exp(-(home_score - away_score)))
        return round(prob * 100, 1)
    except Exception as e:
        return 50.0

# --- 메인 실행부 ---
def main():
    st.title("⚾ MLB 슈퍼컴퓨터 분석 엔진")

    # 1. 경기 목록 (schedule.csv.csv 활용)
    if os.path.exists('schedule.csv.csv'):
        games_df = pd.read_csv('schedule.csv.csv')
        st.write("### 오늘의 경기 일정")
        
        for idx, row in games_df.iterrows():
            home, away = row['home_team'], row['away_team']
            
            # 예측 엔진 가동
            win_prob = get_prediction(home, away)
            
            # UI 출력
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{away} vs {home}**")
            with col2:
                st.metric("홈 승률", f"{win_prob}%")
            st.divider()
    else:
        st.error("schedule.csv.csv 파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
