def process_game_stats(game_data):
    """
    API에서 받은 원본(Raw) 데이터를 분석하기 좋은 표준 지표로 변환
    이 과정에서 40개의 모듈이 사용할 통계 지표(승률, 방어율, 타격감 등)를 추출함
    """
    # 여기서 실제 MLB API 데이터를 해석하여 점수화 가능한 딕셔너리로 반환
    return {
        'home_win_pct': 0.64,
        'away_win_pct': 0.52,
        'home_era': 4.49,
        'away_era': 3.36
        # 여기에 더 많은 통계 지표를 추가
    }
