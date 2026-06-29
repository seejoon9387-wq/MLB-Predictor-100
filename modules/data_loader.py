import pandas as pd
import os
import zipfile
from modules.registry import create_main_registry
# ... (기타 모든 엔진 import 문)

def load_data():
    # 데이터 로드 및 초기화
    if not os.path.exists("mlb_full_data_slim.zip"): return pd.DataFrame()
    with zipfile.ZipFile("mlb_full_data_slim.zip", 'r') as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)
    
    df.columns = [c.lower().strip() for c in df.columns]
    df['is_home_win'] = (df['home_score'] > df['away_score']).astype(int)
    
    # 1. 피처 엔진 파이프라인 (Data Engineering)
    df = process_weather_features(df)
    df = add_stamina_and_limit_features(df)
    df = add_pitch_value_features(df)
    df = add_momentum_features(df)
    df = add_leverage_weighted_stats(df)
    df = add_manager_tendency_features(df)
    df = add_lineup_stability_features(df)
    
    # 2. 통합 레지스트리
    registry = create_main_registry(df)
    return registry
