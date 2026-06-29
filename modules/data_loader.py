import pandas as pd
import os
import zipfile
from modules.registry import create_main_registry
from modules.odds_engine import add_odds_market_features # 추가된 시장 정보 모듈

def load_data():
    if not os.path.exists("mlb_full_data_slim.zip"): return pd.DataFrame()
    with zipfile.ZipFile("mlb_full_data_slim.zip", 'r') as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)
    
    df.columns = [c.lower().strip() for c in df.columns]
    df['is_home_win'] = (df['home_score'] > df['away_score']).astype(int)
    
    # 1. 세이버메트릭스 엔진 통합
    # (기존: 날씨, 스태미나, 투구 가치, 모멘텀, 매니저, 라인업 등)
    # 2. 시장 정보 반영
    df = add_odds_market_features(df)
    
    registry = create_main_registry(df)
    return registry
