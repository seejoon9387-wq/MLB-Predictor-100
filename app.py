import streamlit as st
import pandas as pd
import numpy as np
import os

def get_prediction(home_id, away_id):
    try:
        # 투수 데이터 로드
        pitchers = pd.read_csv('pitchers.csv.csv')
        
        # 'team' 컬럼이 단순 이름이 아니라 ID를 포함할 수 있으므로, 
        # 데이터 내의 team 컬럼을 숫자로 변환하여 비교합니다.
        # 주의: pitchers.csv에 'team_id' 같은 컬럼이 있다면 그 이름을 쓰세요.
        # 여기서는 'team' 컬럼에 ID가 들어있다고 가정합니다.
        
        h_data = pitchers[pitchers['team'].astype(str).str.contains(str(home_id), na=False)]
        a_data = pitchers[pitchers['team'].astype(str).str.contains(str(away_id), na=False)]
        
        if h_data.empty or a_data.empty:
            return 50.0
        
        h_era = pd.to_numeric(h_data['era'], errors='coerce').mean()
        a_era = pd.to_numeric(a_data['era'], errors='coerce').mean()
        
        if np.isnan(h_era) or np.isnan(a_era):
            return 50.0
            
        # 승률 계산: ERA가 낮을수록 유리 (승률 보정 로직)
        prob = 1 / (1 + np.exp(-( (1/(h_era+0.1)) - (1/(a_era+0.1)) )))
        return round(prob * 100, 1)
    except:
        return 50.0

def main():
    st.title("⚾ MLB 슈퍼컴퓨터 분석 엔진")
    
    if os.path.exists('schedule.csv.csv'):
        games_df = pd.read_csv('schedule.csv.csv')
        
        # 데이터프레임의 홈/원정팀 정보가 딕셔너리 형태인지 확인 후 처리
        for idx, row in games_df.iterrows():
            # ID 추출 (만약 딕셔너리라면 id값만 뽑아냄)
            h_id = row['home_team'] if not isinstance(row['home_team'], dict) else row['home_team'].get('id', 0)
            a_id = row['away_team'] if not isinstance(row['away_team'], dict) else row['away_team'].get('id', 0)
            
            # 팀 이름 표시를 위한 정리
            h_name = row['home_team']['name'] if isinstance(row['home_team'], dict) else row['home_team']
            a_name = row['away_team']['name'] if isinstance(row['away_team'], dict) else row['away_team']
            
            win_prob = get_prediction(h_id, a_id)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{a_name} vs {h_name}**")
            with col2:
                st.metric("홈 승률", f"{win_prob}%")
            st.divider()

if __name__ == "__main__":
    main()
