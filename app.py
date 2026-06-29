import streamlit as st
import statsapi
import pandas as pd
import numpy as np
import os

# --- 1. 예측 엔진부 (강력한 이름 매칭 로직 적용) ---
def get_prediction(h_id, a_id, h_p_name, a_p_name):
    try:
        pitchers = pd.read_csv('pitchers.csv.csv')
        batters = pd.read_csv('batters.csv.csv')
        
        def find_pitcher_era(name):
            if name == 'Unknown': return None
            
            # DB 이름 정제: 쉼표 제거, 대소문자 통일
            # API에서 받은 이름(Casey Mize)의 각 단어(Casey, Mize)를 분리
            search_terms = str(name).replace(',', '').split()
            
            # '단어 전체'를 포함하는 행을 찾음 (둘 다 포함해야 함)
            mask = pd.Series([True] * len(pitchers))
            for term in search_terms:
                mask &= pitchers['player'].str.contains(term, case=False, na=False)
            
            match = pitchers[mask]
            return match['era'].mean() if not match.empty else None

        h_era = find_pitcher_era(h_p_name)
        a_era = find_pitcher_era(a_p_name)
        
        if h_era is None or a_era is None: return None
            
        h_off = batters[batters['team'].astype(str).str.contains(str(h_id), na=False)]['ops'].mean()
        a_off = batters[batters['team'].astype(str).str.contains(str(a_id), na=False)]['ops'].mean()
        
        h_score = (1 / (h_era + 0.1) * 0.7) + (h_off * 0.3) + 0.05
        a_score = (1 / (a_era + 0.1) * 0.7) + (a_off * 0.3)
        
        prob = 1 / (1 + np.exp(-(h_score - a_score) * 10))
        return round(prob * 100, 1)
    except Exception as e:
        return None

# --- 2. 메인 실행부 ---
def main():
    st.set_page_config(page_title="MLB 승률 예측 시스템", layout="wide")
    st.title("⚾ 실시간 MLB 승률 예측 엔진")
    
    # 오늘 경기 일정
    games = statsapi.schedule(date=pd.Timestamp.now().strftime('%Y-%m-%d'))

    for game in games:
        h_p = game.get('home_probable_pitcher', 'Unknown')
        a_p = game.get('away_probable_pitcher', 'Unknown')
        
        st.write(f"### {game['away_name']} ({a_p}) vs {game['home_name']} ({h_p})")
        
        win_prob = get_prediction(game['home_id'], game['away_id'], h_p, a_p)
        
        if win_prob is not None:
            st.metric("홈팀 승리 확률", f"{win_prob}%")
        else:
            # 매칭 실패 시 힌트 제공
            st.warning(f"⚠️ 매칭 불가: '{h_p}' 혹은 '{a_p}'의 기록을 DB에서 찾을 수 없습니다.")
        st.divider()

if __name__ == "__main__":
    main()
