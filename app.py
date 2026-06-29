import streamlit as st
import statsapi
import pandas as pd
import numpy as np
import os

# --- 선발 투수 및 전력 기반 예측 엔진 ---
def get_prediction(h_id, a_id, h_pitcher, a_pitcher):
    try:
        # 데이터 로드
        pitchers = pd.read_csv('pitchers.csv.csv')
        batters = pd.read_csv('batters.csv.csv')
        
        # 선발 투수 데이터 찾기 (없으면 에러 발생 유도)
        h_p_data = pitchers[pitchers['player'].str.contains(h_pitcher, na=False, case=False)]
        a_p_data = pitchers[pitchers['player'].str.contains(a_pitcher, na=False, case=False)]
        
        if h_p_data.empty or a_p_data.empty:
            return None # 데이터 없음 반환
            
        # 전력 점수 계산
        h_score = (1 / (h_p_data['era'].mean() + 0.1) * 0.7) + (batters[batters['team'].astype(str).str.contains(str(h_id), na=False)]['ops'].mean() * 0.3)
        a_score = (1 / (a_p_data['era'].mean() + 0.1) * 0.7) + (batters[batters['team'].astype(str).str.contains(str(a_id), na=False)]['ops'].mean() * 0.3)
        
        prob = 1 / (1 + np.exp(-(h_score - a_score) * 10))
        return round(prob * 100, 1)
    except:
        return None

def main():
    st.title("⚾ 실시간 MLB 승률 예측 엔진")
    
    # 1. statsapi로 오늘 경기 가져오기
    try:
        games = statsapi.schedule(date=pd.Timestamp.now().strftime('%Y-%m-%d'))
    except:
        st.error("실시간 경기 정보를 가져올 수 없습니다.")
        return

    for game in games:
        h_name = game['home_name']
        a_name = game['away_name']
        h_id = game['home_id']
        a_id = game['away_id']
        
        # 실시간 선발 투수 정보 추출
        # statsapi는 'home_probable_pitcher', 'away_probable_pitcher' 정보를 제공
        h_p = game.get('home_probable_pitcher', 'Unknown')
        a_p = game.get('away_probable_pitcher', 'Unknown')
        
        st.write(f"### {a_name} ({a_p}) vs {h_name} ({h_p})")
        
        # 2. 엔진 가동 및 결과 확인
        win_prob = get_prediction(h_id, a_id, h_p, a_p)
        
        if win_prob is not None:
            st.metric("홈팀 승리 확률", f"{win_prob}%")
        else:
            st.warning("⚠️ 선발 투수 데이터 부족으로 예측 불가 (DB 확인 필요)")
            
        st.divider()

if __name__ == "__main__":
    main()
