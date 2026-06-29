import pandas as pd

def simulate_match_scenarios(data):
    """
    MLB 경기 시나리오를 시뮬레이션하는 엔진 핵심 모듈
    """
    if isinstance(data, pd.DataFrame):
        # apply 결과에 이름을 부여하여 merge 에러 방지
        results = data.apply(lambda row: _calculate_loc(row), axis=1)
        results.name = 'loc_score' 
        return results
    else:
        # 단일 데이터인 경우 처리
        return _calculate_loc(data)

def _calculate_loc(row):
    # .get() 메서드로 데이터 누락 방지 (KeyError 해결)
    val1 = row.get('bayesian_win_rate', 0.0)
    val2 = row.get('climate_adjusted_prob', 0.0)
    val3 = row.get('inefficiency_score', 0.0)
    
    return val1 + val2 + val3
