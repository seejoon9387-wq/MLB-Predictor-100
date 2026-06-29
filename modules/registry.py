import pandas as pd

def create_main_registry(df):
    """
    원본 df에서 승패 결과를 계산하고, 모델 학습에 필요한 필수 컬럼만 추출하여 레지스트리를 생성합니다.
    """
    # 1. 승패 컬럼이 없다면 생성 (home_score와 away_score를 비교)
    if 'is_home_win' not in df.columns:
        if 'home_score' in df.columns and 'away_score' in df.columns:
            df['is_home_win'] = (df['home_score'] > df['away_score']).astype(int)
        else:
            # 스코어 데이터가 없는 경우를 대비한 예외 처리
            df['is_home_win'] = 0 
    
    # 2. 레지스트리에 포함할 필수 컬럼 정의
    # (추후 머신러닝 학습 시 이 컬럼들을 기반으로 피처를 병합합니다)
    required_cols = [
        'game_pk', 
        'game_date', 
        'game_year', 
        'home_team', 
        'away_team', 
        'is_home_win'
    ]
    
    # 3. 데이터셋에 존재하는 컬럼만 필터링하여 선택
    cols = [c for c in required_cols if c in df.columns]
    
    # 4. 중복 제거 후 레지스트리 반환
    registry = df[cols].drop_duplicates()
    
    return registry
