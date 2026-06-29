def simulate_match_scenarios(data):
    # 가중치 계산식: 베이지안 승률(70%) + 환경 조정(20%) - 비효율(10%)
    b_win = data.get('bayesian_win_rate', 0.5)
    c_adj = data.get('climate_adjusted_prob', 0.1)
    ineff = data.get('inefficiency_score', 0.05)
    
    score = (b_win * 0.7) + (c_adj * 0.2) - (ineff * 0.1)
    return max(0.0, min(1.0, score))
