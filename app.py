import streamlit as st
import pandas as pd
import numpy as np
import os

def get_prediction(home_name, away_name):
    try:
        pitchers = pd.read_csv('pitchers.csv.csv')
        
        # 1. 팀 이름 매칭을 위해 대문자 통일 및 공백 제거
        pitchers['team'] = pitchers['team'].astype(str).str.strip().str.upper()
        home_n = str(home_name).strip().upper()
        away_n = str(away_name).strip().upper()
        
        # 2. 해당 팀의 데이터 필터링
        h_data = pitchers[pitchers['team'].str.contains(home_n[:3], na=False)]
        a_data = pitchers[pitchers['team'].str.contains(away_n[:3], na=False)]
        
        if h_data.empty or a_data.empty:
            return 50.0  # 데이터가 없으면 50% 반환
        
        # 3. ERA 계산 (숫자만 추출)
        h_era = pd.to_numeric(h_data['era'], errors='coerce').mean()
        a_era = pd.to_numeric(a_data['era'], errors='coerce').mean()
        
        if np.isnan(h_era) or np.isnan(a_era):
            return 50.0
            
        # 4. 승률 계산
        prob = 1 / (1 + np.exp(-( (1/(h_era+0.1)) - (1/(a_era+0.1)) )))
        return round(prob * 100, 1)
    except:
        return 50.0

def main():
    st.title("⚾ MLB 슈퍼컴퓨터 분석 엔진")
    
    if os.path.exists('schedule.csv.csv'):
        games_df = pd.read_csv('schedule.csv.csv')
        for idx, row in games_df.iterrows():
            win_prob = get_prediction(row['home_team'], row['away_team'])
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{row['away_team']} vs {row['home_team']}**")
            with col2:
                st.metric("홈 승률", f"{win_prob}%")
            st.divider()

if __name__ == "__main__":
    main()
