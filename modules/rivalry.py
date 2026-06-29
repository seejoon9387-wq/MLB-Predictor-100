import pandas as pd

def calculate_rivalry_factor(df):
    """
    최근 3년간 팀 간 맞대결 승률을 계산하여 천적 관계 지수 생성
    - factor > 1.0: 해당 상대에게 강함
    - factor < 1.0: 해당 상대에게 약함
    """
    # 1. 3년치 데이터 필터링 (예: 2024, 2025, 2026)
    recent_years = [2024, 2025, 2026]
    subset = df[df['game_year'].isin(recent_years)].copy()
    
    # 2. 팀 A vs 팀 B 승패 기록 집계
    rivalry_stats = subset.groupby(['home_team', 'away_team'])['is_home_win'].agg(['mean', 'count']).reset_index()
    rivalry_stats.columns = ['home_team', 'away_team', 'win_rate', 'game_count']
    
    # 3. 데이터 병합을 위한 룩업 테이블 생성
    return rivalry_stats

def add_rivalry_features(registry, df):
    stats = calculate_rivalry_factor(df)
    # registry에 'home_team'과 'away_team' 기준 매핑
    registry = registry.merge(stats, on=['home_team', 'away_team'], how='left').fillna(0.5)
    return registry
