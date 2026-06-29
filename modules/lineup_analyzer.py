# modules/lineup_analyzer.py
import numpy as np

def calculate_lineup_sensitivity(df, lineup_columns, key_players):
    """
    핵심 타자 결장 시 득점 변화 분석
    - lineup_columns: 라인업에 포함된 타자 식별자 리스트
    - key_players: 핵심 타자(시뮬레이션 대상) 리스트
    """
    results = {}
    
    # 1. 베이스라인: 현재 득점 생산력(wOBA 등 활용)
    baseline_score = df['estimated_woba_using_speedangle'].mean()
    
    for player in key_players:
        # 2. 핵심 타자 제외 시 데이터 필터링
        df_no_player = df[df['batter'] != player]
        
        # 3. 득점력 급락 정도 계산
        new_score = df_no_player['estimated_woba_using_speedangle'].mean()
        drop_rate = (baseline_score - new_score) / baseline_score
        
        results[player] = drop_rate
        
    return results

def simulate_lineup_impact(df, drop_rate_map):
    #
