import pandas as pd

def simulate_match_scenarios(data):
    """
    MLB 경기 시나리오를 시뮬레이션하는 엔진 핵심 모듈
    데이터 접근 시 .get() 방식을 사용하여 KeyError를 방지합니다.
    """
    # 데이터가 DataFrame인 경우와 단일 딕셔너리인 경우 모두 처리
    if isinstance(data, pd.DataFrame):
        results = data.apply(lambda row: _calculate_loc(row), axis=1)
    else:
        results = _calculate_loc(data)
        
    return results

def _calculate_loc(row):
    """
    데이터 키 접근 시 방어적 로직을 적용한 계산 함수
    (이 부분이 18행 오류를 해결하는 핵심입니다)
    """
    # .get() 메서드를 사용하여 키가 없으면 0.0을 반환하도록 수정
    val1 = row.get('bayesian_win_rate', 0.0)
    val2 = row.get('climate_adjusted_prob', 0.0)
    val3 = row.get('inefficiency_score', 0.0)
    
    loc = val1 + val2 + val3
    
    # 추가적인 분석 로직이 있다면 여기에 작성
    return loc

# 필요에 따라 아래와 같은 추가 분석 함수들을 이어서 작성하세요.
