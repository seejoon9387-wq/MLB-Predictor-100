import streamlit as st
import statsapi
import pandas as pd
import numpy as np
import os

# --- 1. 예측 엔진부 ---
def get_prediction(h_id, a_id, h_p_data_api, a_p_data_api):
    try:
        if not os.path.exists('pitchers.csv.csv') or not os.path.exists('batters.csv.csv'):
            return None
            
        pitchers = pd.read_csv('pitchers.csv.csv')
        batters = pd.read_csv('batters.csv.csv')
        
        # --- 이름 조합 검색 로직 ---
        def find_pitcher_stats(p_api):
            # p_api가 딕셔너리(API 형태)면 이름 조합, 아니면 기존 문자열 검색
            if isinstance(p_api, dict):
                full_name = f"{p_api.get('firstName', '')} {p_api.get('lastName', '')}".strip()
            else:
                full_name = str(p_api)
                
            if full_name == 'Unknown' or not full_name: return None
            
            # DB의 'player' 컬럼과 완전 일치 검색
            match = pitchers[pitchers['player'].str.contains(full_name, na=False, case=False)]
            return match['era'].mean() if not match.empty else None

        h_era = find_pitcher_stats(h_p_data_api)
        a_era = find_pitcher_stats(a_p_data_api)
        
        if h_era is None or a_era is None: return None
            
        # 전력 점수 계산
        h_off = batters[batters['team'].astype(str).str.contains(str(h_id), na=False)]['ops'].mean()
        a_off = batters[batters['team'].astype(str).str.contains(str(a_id), na=False)]['ops'].mean()
        
        h_score = (1 / (h_era + 0.1) * 0.7) + (h_off * 0.3) + 0.05
        a_score = (1 / (a_era + 0.1) * 0.7) + (a_off * 0.3)
        
        prob = 1 / (1 + np.exp(-(h_score - a_score) * 10))
        return round(prob * 100, 1)
    except:
        return None

# --- 2. 메인 실행부 (UI) ---
def main():
    st.set_page_config(page_title="MLB 승률 예측 시스템", layout="wide")
    st.title("⚾ 실시간 MLB 승률 예측 엔진")
    
    games = statsapi.schedule(date=pd.Timestamp.now().strftime('%Y-%m-%d'))

    for game in games:
        h_name, a_name = game['home_name'], game['away_name']
        h_id, a_id = game['home_id'], game['away_id']
        
        # 선발 투수 정보를 객체 형태로 가져오기 (이름 결합용)
        h_p_name = game.get('home_probable_pitcher', 'Unknown')
        a_p_name = game.get('away_probable_pitcher', 'Unknown')
        
        st.write(f"### {a_name} ({a_p_name}) vs {h_name} ({h_p_name})")
        
        win_prob = get_prediction(h_id, a_id, h_p_name, a_p_name)
        
        if win_prob is not None:
            st.metric("홈팀 승리 확률", f"{win_prob}%")
        else:
            st.warning(f"⚠️ 매칭 실패: '{h_p_name}' 또는 '{a_p_name}'을 DB에서 찾을 수 없습니다.")
        st.divider()

if __name__ == "__main__":
    main()
