import pandas as pd
import os
import zipfile
from modules.odds_engine import add_odds_market_features
from modules.bayesian_updater import get_bayesian_win_prob

def load_data(analysis_mode=False):
    if not os.path.exists("mlb_full_data_slim.zip"): 
        print("파일을 찾을 수 없습니다.")
        return pd.DataFrame()
        
    with zipfile.ZipFile("mlb_full_data_slim.zip", 'r') as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)
    
    # 데이터 통계 확인
    print(f"로드된 전체 데이터 행 수: {len(df)}")
    print(f"고유 경기(game_pk) 수: {df['game_pk'].nunique() if 'game_pk' in df.columns else '없음'}")
    
    df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
    
    if 'home_score' in df.columns and 'away_score' in df.columns:
        df['is_home_win'] = (df['home_score'] > df['away_score']).astype(int)
    
    # 베이지안 보정
    df['bayesian_win_rate'] = df.apply(lambda x: get_bayesian_win_prob(x.get('home_score', 0), 1), axis=1)
    
    # 시장 정보 적용
    df = add_odds_market_features(df)
    
    return df
