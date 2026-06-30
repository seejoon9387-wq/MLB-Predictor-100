import numpy as np
import pandas as pd
from scipy.stats import linregress

class PlayerProfiler:
    def __init__(self, window_weights=None):
        # 1일, 3일, 7일 기간에 대한 기본 가중치 (필요시 백테스팅 결과로 갱신)
        self.window_weights = window_weights or {1: 0.2, 3: 0.3, 7: 0.5}

    def _get_slope(self, data, window, feature):
        """단일 기간에 대한 선형 회귀 기울기 산출"""
        if len(data) < window:
            return 0.0
        
        recent_data = data.tail(window)
        y = recent_data[feature].values
        x = np.arange(len(y))
        
        slope, _, _, _, _ = linregress(x, y)
        return slope

    def calculate_integrated_condition_index(self, df_player, feature='ops'):
        """
        1, 3, 7일 기간별 기울기를 유기적으로 결합하여 최종 컨디션 지수 산출
        - 1일: 단기 모멘텀
        - 3일: 중기 조정
        - 7일: 추세 지속성
        """
        # 각 기간별 기울기 산출
        slopes = {
            1: self._get_slope(df_player, 1, feature),
            3: self._get_slope(df_player, 3, feature),
            7: self._get_slope(df_player, 7, feature)
        }
        
        # 유기적 가중치 합산 (Condition Index 도출)
        condition_index = sum(slopes[w] * self.window_weights[w] for w in self.window_weights)
        
        return {
            'index': condition_index,
            'details': slopes
        }

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    # 테스트용 가상 데이터 생성 (최근 7경기 OPS 변화)
    test_data = pd.DataFrame({'ops': [0.700, 0.720, 0.710, 0.750, 0.740, 0.780, 0.800]})
    
    profiler = PlayerProfiler()
    result = profiler.calculate_integrated_condition_index(test_data, feature='ops')
    
    print(f"산출된 최종 컨디션 지수: {result['index']:.4f}")
    print(f"기간별 상세 기울기: {result['details']}")
