# modules/briefing_engine.py (전체 코드)
def generate_match_briefing(game_pk, df):
    match = df[df['game_pk'] == game_pk].iloc[0]
    
    briefing = f"""
    --- [MLB 경기 상세 분석 브리핑: Game ID {game_pk}] ---
    1. 통계적 안정성: 베이지안 보정 승률 {match['bayesian_win_rate']:.2%}
    2. 기상/환경 보정: {match['temp_factor']:.2f} (온도/풍향 영향 반영)
    3. 라인업 민감도: 핵심 타자 결장 시 득점력 변화 {match.get('adjusted_run_exp', 0):.2f}
    4. 시장 비효율성: Inefficiency Score {match['inefficiency_score']:.4f} 
       - 대중 편향 여부: {'Yes' if match['is_public_bias'] else 'No'}
    5. 최종 몬테카를로 결과: 승리 확률 {match['sim_win_prob']:.2%}, 기대 수익 {match['expected_value']:.4f}
    
    [결론] { '베팅 권장(Value Detected)' if match['expected_value'] > 0 else '베팅 보류(Low Value)' }
    """
    return briefing
