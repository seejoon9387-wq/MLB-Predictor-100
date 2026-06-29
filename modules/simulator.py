# modules/simulator.py (전체 코드)
import numpy as np
import pandas as pd

def simulate_match_scenarios(df, iterations=100000):
    """
    모든 변수를 결합하여 10만 번의 경기 시나리오 생성
    """
    results = []
    
    for i in range(len(df)):
        # 개별 경기 데이터 추출
        row = df.iloc[i]
        
        # 몬테카를로 시뮬레이션 수행
        # 베이지안 확률 + 날씨 영향 + 라인업 공백 + 시장 편향을 결합한 득점 분포
        sim_scores = np.random.normal(
            loc=row['bayesian_win_rate'] + row['climate_adjusted_prob'] + row['inefficiency_score'],
            scale=0.15, # 경기 내 변동성(Volatility)
            size=iterations
        )
        
        # 시나리오 결과: 승률(득점 확률 기반) 및 수익 기대값
        win_prob = np.mean(sim_scores > 0.5)
        results.append({
            'game_pk': row['game_pk'],
            'sim_win_prob': win_prob,
            'sim_std_dev': np.std(sim_scores), # 예측 불확실성(위험도)
            'expected_value': (win_prob * row.get('current_home_odds', 2.0)) - 1
        })
        
    return pd.DataFrame(results)
