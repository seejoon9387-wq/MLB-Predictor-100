# modules/environment_booster.py

def apply_park_factor(df, home_team):
    """구장별 득점 환경 팩터 반영"""
    # 임시 매핑 테이블 (실제 데이터에 맞게 최신 수치로 업데이트 필요)
    park_factors = {'COL': 1.15, 'SF': 0.92, 'NYY': 1.05} 
    factor = park_factors.get(home_team, 1.0)
    df['woba_value'] = df['woba_value'] * factor
    return df

def calculate_leverage_index(balls, strikes, outs, inning):
    """상황 중요도(LI) 계산: 대략적인 상황 보정 가중치"""
    # 9회말, 점수차 1점, 주자 만루 등 상황에 따른 가중치 로직
    base_weight = 1.0
    if inning >= 8: base_weight += 0.5
    if outs == 2: base_weight += 0.2
    return base_weight
