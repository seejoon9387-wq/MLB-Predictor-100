import pandas as pd

def simulate_match_scenarios(data):
    """
    MLB 경기 시나리오를 시뮬레이션하는 엔진 핵심 모듈
    데이터 접근 시 .get() 방식을 사용하여 KeyError를 방지하고,
    가중치 계산을 통해 더 정교한 분석 결과를 도출합니다.
    """
    # 데이터가 DataFrame인 경우와 단일 딕셔너리인 경우 모두 처리
    if isinstance(data, pd.DataFrame):
        results = data.apply(lambda row: _calculate_loc(row), axis=1)
        results.name = 'loc_score'
        return results
    else:
        return _calculate_loc(data)

def _calculate_loc(row):
    """
    가중치가 적용된 정교한 승률 계산 함수 (가중치 합산 방식)
    데이터가 없으면 기본값을 사용하여 계산 안정성을 확보합니다.
    """
    # 1. 입력 데이터 추출 (누락 시 기본값 적용)
    b_win = row.get('bayesian_win_rate', 0.5)      # 베이지안 승률 (가중치 70%)
    c_adj = row.get('climate_adjusted_prob', 0.1)  # 기후/환경 조정 (가중치 20%)
    ineff = row.get('inefficiency_score', 0.05)    # 비효율 지수 (가중치 10% 감점)
    
    # 2. 정교화된 가중치 계산식
    # 단순히 더하는 것이 아니라 통계적 가중치를 적용하여 0.0~1.0 사이로 조정
    score = (b_win * 0.7) + (c_adj * 0.2) - (ineff * 0.1)
    
    # 3. 결과 반환
    return max(0.0, min(1.0, score))
