# modules/matchup.py

def get_platoon_advantage(pitcher_hand, batter_hand):
    """좌우 상성(Platoon) 가중치 산출"""
    # 같은 손이면 투수 우위, 다르면 타자 우위 가정 (데이터로 정교화 필요)
    if pitcher_hand == batter_hand:
        return 0.95  # 투수 우위
    return 1.05      # 타자 우위

def calculate_lineup_synergy(batters_stats):
    """라인업 시너지: 앞 타자의 출루율이 뒷 타자에게 미치는 영향"""
    # 1번부터 9번 타자까지의 OBP(출루율)를 기반으로 시너지 지수 계산
    synergy_score = 0
    for i in range(1, len(batters_stats)):
        # 앞 타자의 출루율이 높을수록 뒷 타자의 타점 기회 상승
        synergy_score += (batters_stats[i-1]['obp'] * batters_stats[i]['woba'])
    return synergy_score / len(batters_stats)
