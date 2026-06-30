import pandas as pd

def get_stamina_adjustment(pitcher_data):
    """
    투수의 피로도 정보를 받아 승률 보정치를 반환
    pitcher_data 구조: {
        'last_pitch_count': int,  # 최근 경기 투구 수
        'days_rest': int          # 휴식 일수
    }
    """
    pitch_count = pitcher_data.get('last_pitch_count', 0)
    days_rest = pitcher_data.get('days_rest', 4)
    
    adjustment = 0.0
    
    # 1. 투구 수가 많으면 피로도 가중치 (마이너스 보정)
    if pitch_count > 100:
        adjustment -= 0.03
    elif pitch_count > 80:
        adjustment -= 0.01
        
    # 2. 휴식 일수가 짧으면 피로도 가중치 (마이너스 보정)
    if days_rest < 3:
        adjustment -= 0.02
    elif days_rest >= 5:
        adjustment += 0.01
        
    return max(-0.07, min(0.03, adjustment)) # 보정 범위 제한
