import pandas as pd

def apply_platoon_weights(df):
    """
    타자/투수 좌우 상성(Platoon)을 계산하여 가중치 컬럼 추가
    - 1.0: 동일 방향 (상성 우위/열위 여부)
    - 1.05 ~ 1.10: 상성 우위 (가중치 적용)
    """
    # 기본 가중치 설정
    # 'L' vs 'L' 혹은 'R' vs 'R'은 동일 방향 (Base)
    # 'L' vs 'R' 혹은 'R' vs 'L'은 상성 우위 (Platoon Advantage)
    
    def get_platoon_factor(row):
        batter_side = row.get('stand', 'R')
        pitcher_side = row.get('p_throws', 'R')
        
        # 좌투좌타/우투우타 (일반) vs 좌투우타/우투좌타 (플래툰)
        if batter_side != pitcher_side:
            return 1.08  # 상성 우위 시 타자 성적 가중치 8% 향상 가정
        return 1.0
    
    df['platoon_factor'] = df.apply(get_platoon_factor, axis=1)
    
    # 보정된 woba 계산
    if 'woba_value' in df.columns:
        df['adj_woba'] = df['woba_value'] * df['platoon_factor']
        
    return df
