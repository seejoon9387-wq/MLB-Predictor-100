import pandas as pd

def get_team_matchup_adjustment(lineup_data, pitcher_data):
    """
    오늘의 라인업과 상대 투수 정보를 받아 팀 단위 상성 보정치를 반환
    """
    # 1. 라인업 각 타자의 vs_pitcher_woba를 평균
    # 2. 이 값이 리그 평균보다 높으면 승리 확률 + 가중치
    avg_woba = lineup_data['vs_pitcher_woba'].mean()
    league_avg_woba = 0.320 # 기준값
    
    # 상성 보정치 계산: 평균 woba가 높으면 승률 긍정 보정
    adjustment = (avg_woba - league_avg_woba) * 2
    return adjustment
