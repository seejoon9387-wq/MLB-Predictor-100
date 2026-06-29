import streamlit as st
import statsapi
import pandas as pd
import numpy as np
import os

# --- 1. 예측 엔진부 ---
def get_prediction(h_id, a_id, h_pitcher, a_pitcher):
    try:
        # 데이터가 경로에 정확히 있는지 다시 한번 확인
        pitchers = pd.read_csv('pitchers.csv.csv')
        batters = pd.read_csv('batters.csv.csv')
        
        # --- 고도화된 이름 매칭 함수 ---
        def find_pitcher_stats(full_name):
            if full_name == 'Unknown': return None
            
            # 검색을 위한 이름 분해
            name_parts = str(full_name).split()
            first = name_parts[0]
            last = name_parts[-1]
            
            # 1. 'First Last' 검색
            match = pitchers[pitchers['player'].str.contains(f"{first}.*{last}", na=False, case=False)]
            
            # 2. 실패 시 'Last, First' 검색 (데이터가 성, 이름 순일 경우 대비)
            if match.empty:
                match = pitchers[pitchers['player'].str.contains(f"{last}.*{first}", na=False, case=False)]
                
            return match['era'].mean() if not match.empty else None

        h_era = find_pitcher_stats(h_pitcher)
        a_era = find_pitcher_stats(a_pitcher)
        
        if h_era is None or a_era is None: return None
            
        # 전력 점수 계산
        h_off = batters[batters['team'].astype(str).str.contains(str(h_id), na=False)]['ops'].mean()
        a_off = batters[batters['team'].astype(str).str.contains(str(a_id), na=False)]['ops'].mean()
        
        h_score = (1 / (h_era + 0.1) * 0.7) + (h_off * 0.3) + 0.05
        a_score = (1 / (a_era + 0.1) * 0.7) + (a_off * 0.3)
        
        prob = 1 / (1 + np.exp(-(h_score - a_score) * 10))
        return round(prob * 100, 1)
    except Exception as e:
        return None

# --- 2. 메인 실행부 (UI) ---
def main():
    st.set_page_config(page_title="MLB 승률 예측 시스템", layout="wide")
    st.title("⚾ 실시간 MLB 승률 예측 엔진")
    
    try:
        games = statsapi.schedule(date=pd.Timestamp.now().strftime('%Y-%m-%d'))
    except:
        st.error("MLB 서버 연결 실패")
        return

    for game in games:
        h_name, a_name = game['home_name'], game['away_name']
        h_id, a_id = game['home_id'], game['away_id']
        h_p = game.get('home_probable_pitcher', 'Unknown')
        a_p = game.get('away_probable_pitcher', 'Unknown')
        
        st.write(f"### {a_name} ({a_p}) vs {h_name} ({h_p})")
        
        win_prob = get_prediction(h_id, a_id, h_p, a_p)
        
        if win_prob is not None:
            st.metric("홈팀 승리 확률", f"{win_prob}%")
        else:
            # 매칭 실패 시 디버깅을 위해 DB상의 어떤 이름과 비교했는지 힌트 제공
            st.warning(f"⚠️ 매칭 실패: '{h_p}' 또는 '{a_p}'를 DB에서 찾을 수 없습니다. (이름 표기법 확인 필요)")
        st.divider()

if __name__ == "__main__":
    main()
