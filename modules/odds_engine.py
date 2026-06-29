def add_odds_market_features(df):
    # 실제 데이터셋의 컬럼명으로 자동 매핑 (데이터에 맞춰 이름 수정하세요)
    mapping = {
        'current_home_odds': ['home_odds', 'current_odds', 'home_price'],
        'opening_home_odds': ['opening_odds', 'open_odds', 'initial_price']
    }
    
    # 존재하는 컬럼을 찾아 매핑
    for target, candidates in mapping.items():
        for cand in candidates:
            if cand in df.columns:
                df[target] = df[cand]
                break
        
        if target not in df.columns:
            # 필수 컬럼이 없을 경우 예외 처리
            raise KeyError(f"필수 배당 컬럼 '{target}'을 찾을 수 없습니다. "
                           f"데이터의 컬럼명: {df.columns.tolist()}")

    # 시장 정보 계산
    df['odds_movement'] = (df['current_home_odds'] - df['opening_home_odds']) / df['opening_home_odds']
    df['market_win_prob'] = 1 / df['current_home_odds']
    
    # 모델 예측값과의 차이를 계산하기 위해 임시 컬럼 생성 (모델 학습 후 채워짐)
    if 'model_base_win_prob' not in df.columns:
        df['model_base_win_prob'] = 0.5 
        
    df['odds_discrepancy'] = df['market_win_prob'] - df['model_base_win_prob']
    return df
