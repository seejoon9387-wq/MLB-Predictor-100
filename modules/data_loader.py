import pandas as pd
import os
import zipfile
from modules.registry import create_main_registry
# ... (엔진 모듈들)

def load_data():
    if not os.path.exists("mlb_full_data_slim.zip"): return pd.DataFrame()
    with zipfile.ZipFile("mlb_full_data_slim.zip", 'r') as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)
    
    df.columns = [c.lower().strip() for c in df.columns]
    df['is_home_win'] = (df['home_score'] > df['away_score']).astype(int)
    
    # 세이버메트릭스 엔진 통합 파이프라인
    engines = [
        process_weather_features, add_stamina_and_limit_features, 
        add_pitch_value_features, add_momentum_features, 
        add_leverage_weighted_stats, add_manager_tendency_features, 
        add_lineup_stability_features, add_defensive_efficiency, 
        add_catcher_impact_features
    ]
    for engine in engines:
        df = engine(df)
        
    registry = create_main_registry(df)
    return registry
