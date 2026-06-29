import pandas as pd

def normalize_text_data(df):
    """
    데이터셋의 주요 텍스트 컬럼을 정규화합니다.
    - 소문자 변환
    - 양끝 공백 제거
    - 불필요한 특수문자 제거
    """
    text_cols = ['player_name', 'home_team', 'away_team']
    
    for col in text_cols:
        if col in df.columns:
            # 1. 문자열로 변환 후 공백 제거 및 소문자화
            df[col] = df[col].astype(str).str.strip().str.lower()
            
            # 2. 'los angeles dodgers' 같은 팀명을 'la dodgers'로 통일하는 등 
            # 필요에 따라 매핑 작업 추가 가능
            mapping = {
                'los angeles dodgers': 'la dodgers',
                'new york yankees': 'ny yankees',
                # 추가적인 팀명 통일 작업...
            }
            df[col] = df[col].replace(mapping)
            
    return df
