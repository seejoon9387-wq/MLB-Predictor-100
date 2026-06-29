import streamlit as st
import pandas as pd
import numpy as np
import os

# --- 엔진: 승률 예측 알고리즘 ---
def get_prediction(home_id, away_id):
    try:
        # 데이터가 있는 폴더에서 파일 로드
        if not os.path.exists('pitchers.csv.csv') or not os.path.exists('batters.csv.csv'):
            return 50.0
            
        pitchers = pd.read_csv('pitchers.csv.csv')
        batters = pd.read_csv('batters.csv.csv')
        
        # 데이터 클렌징 (팀 정보 매칭)
        def get_offense(t_id):
            b_data = batters[batters['team'].astype(str).str.contains(str(t_id), na=False)]
            # OPS가 높을수록 공격력 강함
            return b_data['ops'].mean() if not b_data.empty else 0.730 
        
        def get_defense(t_id):
            p_data = pitchers[pitchers['team'].astype(str).str.contains(str(t_id), na=False)]
            # ERA가 낮을수록 투수력이 강함
            era_val = p_data['era'].mean() if not p_data.empty else 4.0
            return 1 / (era_val + 0.5)
            
        # 3중 가중치 계산: 공격(60%) + 수비(40%) + 홈어드밴티지(5%)
        home_score = (get_offense(home_id) * 0.6) + (get_defense(home_id) * 0.4) + 0.05
        away_score = (get_offense(away_id) * 0.6) + (get_defense(away_id) * 0.4)
        
        # 로지스틱 함수로 승률 변환 (10배 증폭하여 확률 차이를 명확히 함)
        prob = 1 / (1 + np.exp(-(home_score - away_score) * 10))
        return round(prob * 100, 1)
    except:
        return 50.0

# --- UI: 화면 출력부 ---
def main():
    st.set_page_config(page_title="MLB 예측 엔진", layout="wide")
    st.title("⚾ MLB 슈퍼컴퓨터 분석 엔진")
    st.write("---")

    if os.path.exists('schedule.csv.csv'):
        games_df = pd.read_csv('schedule.csv.csv')
        
        for idx, row in games_df.iterrows():
            # 데이터에서 ID와 이름 추출
            h_val = row['home_team']
            a_val = row['away_team']
            
            # ID/이름 구분 처리
            h_id = h_val.get('id', 0) if isinstance(h_val, dict) else h_val
            a_id = a_val.get('id', 0) if isinstance(a_val, dict) else a_val
            h_name = h_val.get('name', 'Home') if isinstance(h_val, dict) else h_val
            a_name = a_val.get('name', 'Away') if isinstance(a_val, dict) else a_val
            
            # 예측 실행
            win_prob = get_prediction(h_id, a_id)
            
            # 화면 표시
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"### {a_name} vs {h_name}")
            with col2:
                st.metric("홈팀 승리 확률", f"{win_prob}%")
            st.divider()
    else:
        st.error("데이터 파일(schedule.csv.csv 등)을 찾을 수 없습니다. 경로를 확인해주세요.")

if __name__ == "__main__":
    main()
