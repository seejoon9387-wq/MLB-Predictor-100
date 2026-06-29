# modules/leverage_engine.py
import pandas as pd

def add_leverage_weighted_stats(df):
    """
    고압박 상황(High Leverage)의 성적에 가중치를 부여한 지표 생성
    """
    # High Leverage(LI > 1.5)인 상황의 성적 비중 계산
    # df에 leverage_index, is_high_leverage 컬럼이 있다고 가정
    
    # 1. 승부처 상황에서의 성적 추출 및 가중치 적용
    df['high_leverage_weight'] = df['leverage_index'].apply(lambda x: 1.5 if x > 1.5 else 1.0)
    
    # 2. 가중치가 반영된 타격/투구 지표 계산
    # 예: 가중 OPS = (기본 OPS) * (승부처 상황 가중치)
    df['weighted_ops'] = df['ops'] * df['high_leverage_weight']
    df['weighted_fip'] = df['fip'] * df['high_leverage_weight']
    
    # 3. 최근 20경기 승부처 상황 집중도(Clutch Performance) 지표
    df = df.sort_values(['team_id', 'date'])
    df['clutch_performance_index'] = df.groupby('team_id')['weighted_ops'].transform(
        lambda x: x.rolling(20, min_periods=1).mean()
    )
    
    return df
