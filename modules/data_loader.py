import pandas as pd
import os
import zipfile
from modules.odds_engine import add_odds_market_features
from modules.bayesian_updater import get_bayesian_win_prob
from modules.data_manager import DataManager

def load_data(file_path="mlb_full_data_slim.zip"):
    """데이터 로드 및 기본 정제 (추론 엔진용)"""
    if not os.path.exists(file_path): 
        return pd.DataFrame()
        
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)
    
    # 1. 컬럼명 정제
    df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
    
    # 2. DataManager의 검증 로직 적용
    return DataManager.validate_data(df)

def prepare_inference_features(data_dict):
    """
    추론 전 입력 데이터를 분석 가능한 형태(Feature Set)로 변환
    data_dict: 입력받은 경기 데이터 딕셔너리
    """
    # 1. 시장 정보 적용
    data_dict = add_odds_market_features(data_dict)
    
    # 2. 베이지안 승률 업데이트
    # 과거 경기 이력 등 베이지안 업데이트에 필요한 인자 전달
    prior_win = data_dict.get('prior_win_rate', 0.5)
    current_obs = data_dict.get('home_score', 0)
    data_dict['bayesian_win_rate'] = get_bayesian_win_prob(current_obs, prior_win)
    
    return data_dict
