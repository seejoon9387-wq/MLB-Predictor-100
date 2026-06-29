import pandas as pd
import os
import zipfile
from modules.registry import create_main_registry
from modules.odds_engine import add_odds_market_features
from modules.bayesian_updater import get_bayesian_win_prob

def load_data(analysis_mode=False): # 인자 추가
    if analysis_mode:
        print("모드: 데이터 분석 최적화 모드 활성화")
        
    if not os.path.exists("mlb_full_data_slim.zip"): 
        return pd.DataFrame()
        
    with zipfile.ZipFile("mlb_full_data_slim.zip", 'r') as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)
    
    df.columns = [c.lower().strip() for c in df.columns]
    df['is_home_win'] = (df['home_score'] > df['away_score']).astype(int)
    
    # 베이지안 보정 피처 생성
    df['bayesian_win_rate'] = df.apply(
        lambda x: get_bayesian_win_prob(x.get('team_wins', 0), x.get('team_games', 1)), axis=1
    )
    
    # 시장 정보 엔진 적용
    df = add_odds_market_features(df)
    
    return create_main_registry(df)
# data_loader.py의 load_data 함수 내부에 추가
print(f"로드된 전체 데이터 행 수: {len(df)}")
