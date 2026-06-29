# modules/odds_engine.py 수정
def add_odds_market_features(df):
    """
    배당 컬럼이 없는 경우, 승리 기대 확률(home_win_exp)을 기반으로 시장 정보 추정
    """
    # 배당 데이터가 없을 때 승리 기대 확률을 시장 정보로 대신 사용
    if 'home_win_exp' in df.columns:
        # 시장 확률을 기대 승률로 대체
        df['market_win_prob'] = df['home_win_exp']
        # 변화율 대신 승리 확률의 증분(delta_home_win_exp) 활용
        df['odds_movement'] = df['delta_home_win_exp'] 
    else:
        # 둘 다 없으면 0.5로 강제 설정하여 오류 방지
        df['market_win_prob'] = 0.5
        df['odds_movement'] = 0.0
    
    df['odds_discrepancy'] = df['market_win_prob'] - 0.5 # 베이스라인 비교
    
    return df
