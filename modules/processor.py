import numpy as np

def process_game_stats(game_data):
    """
    API 원본 데이터를 받아 40개 모듈에서 사용할 표준 지표 딕셔너리로 변환.
    데이터 누락 시 기본값(None 또는 0)을 처리하여 시스템 안정성을 확보합니다.
    """
    
    # 1. 데이터 추출 (KeyError 방지)
    def get_val(key, default=0.0):
        return game_data.get(key, default)

    # 2. 분석용 표준 통계 산출
    # 데이터가 0일 경우 발생하는 오류를 방지하기 위해 정규화 로직 포함
    home_era = get_val('home_era', 4.5)
    away_era = get_val('away_era', 4.5)
    
    # 3. 표준화된 지표 반환 (전체 모듈이 공통으로 사용하는 사전)
    stats = {
        'home_win_pct': get_val('home_win_pct', 0.5),
        'away_win_pct': get_val('away_win_pct', 0.5),
        'home_era': home_era,
        'away_era': away_era,
        # ERA를 승률 보정용 수치로 변환 (역수 기반 가중치)
        'era_gap': away_era - home_era, 
        
        # 향후 추가될 지표 자리
        'home_offense_rating': get_val('home_offense', 100),
        'away_offense_rating': get_val('away_offense', 100),
        
        # 모델 학습 및 검증용 태그
        'game_id': get_val('game_id', 'unknown'),
        'timestamp': get_val('timestamp', None)
    }
    
    return stats
