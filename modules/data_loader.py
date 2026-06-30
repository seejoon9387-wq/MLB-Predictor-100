import pandas as pd
import os
import zipfile
from modules.odds_engine import add_odds_market_features
from modules.bayesian_updater import get_bayesian_win_prob

def load_data(file_path="mlb_full_data_slim.zip"):
    """데이터 로드 및 기본 정제 (추론 엔진용)"""
    if not os.path.exists(file_path): 
        return pd.DataFrame()
        
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)
    
    # 1. 표준화: 컬럼명 정제
    df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
    return df

def prepare_inference_features(df_row):
    """추론 전 단일 행에 대한 보정 로직 적용"""
    # 1. 시장 정보 적용
    df_row = add_odds_market_features(df_row)
    
    # 2. 베이지안 보정 적용
    # 주의: get_bayesian_win_prob 인자 전달 방식 확인 필요
    df_row['bayesian_win_rate'] = get_bayesian_win_prob(df_row.get('home_score', 0), 1)
    
    return df_row
