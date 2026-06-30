import numpy as np

def calculate_lineup_sensitivity(df, key_players):
    """핵심 타자 결장 시 득점 변화(drop_rate) 계산"""
    results = {}
    baseline_score = df['estimated_woba_using_speedangle'].mean()
    
    for player in key_players:
        df_no_player = df[df['batter'] != player]
        new_score = df_no_player['estimated_woba_using_speedangle'].mean()
        drop_rate = (baseline_score - new_score) / baseline_score
        results[player] = drop_rate
    return results

def simulate_lineup_impact(current_lineup, drop_rate_map):
    """
    현재 출전 명단과 결장 선수 정보를 비교하여 최종 승률 보정치를 반환
    - current_lineup: [선수1, 선수2, ...]
    - drop_rate_map: {선수명: 결장 시 득점 하락폭}
    """
    total_adjustment = 0.0
    for player in current_lineup:
        # 만약 해당 선수가 결장자 명단에 있다면 하락폭만큼 승률에서 차감
        if player in drop_rate_map:
            total_adjustment -= drop_rate_map[player] * 0.1 # 보정 계수 적용
            
    return max(-0.05, min(0, total_adjustment)) # 보정치 제한
