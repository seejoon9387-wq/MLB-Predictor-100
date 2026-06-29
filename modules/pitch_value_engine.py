# modules/pitch_value_engine.py
import pandas as pd

def add_pitch_value_features(df):
    """
    구종별 가치(Run Value per 100 pitches) 상세 분류
    """
    # 구종 리스트 (데이터셋에 있는 구종 코드에 맞춰 수정 가능)
    pitch_types = ['ff', 'sl', 'cu', 'ch', 'si']
    
    for pt in pitch_types:
        # 특정 구종의 가치를 100구당 득점 억제값으로 산출
        # df[f'{pt}_run_value']가 이미 존재한다고 가정 (데이터 로더에서 제공)
        df[f'{pt}_value_index'] = df[f'{pt}_run_value'] * df[f'{pt}_usage_rate']
        
    # 투수별 최고 주무기 구종 가치 산출
    cols = [f'{pt}_value_index' for pt in pitch_types]
    df['best_pitch_value'] = df[cols].max(axis=1)
    
    # 구종 믹스 다양성 지표 (엔트로피 개념 적용)
    df['pitch_mix_diversity'] = df[cols].std(axis=1)
    
    return df
