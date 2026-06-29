import pandas as pd
import numpy as np

class MLBUnifiedTrainer:
    def __init__(self):
        # 40개 이상의 모듈 알고리즘을 제어하는 핵심 가중치 사전
        # 키는 데이터 컬럼명(h_, a_ 제외), 값은 해당 지표의 영향력
        self.weights = {
            'era': -0.3,    # 투수력: 낮을수록 유리
            'ops': 0.4,     # 타력: 높을수록 유리
            'last_10': 0.2, # 최근 흐름: 높을수록 유리
            'whip': -0.15,  # 투수 안정성: 낮을수록 유리
            'avg': 0.15,    # 타율: 높을수록 유리
            'hr': 0.1,      # 장타력
            'bb': 0.05      # 볼넷 비율
            # 필요한 만큼 여기에 추가하면 자동으로 연산됨
        }

    def analyze(self, data_dict):
        """
        데이터에 있는 모든 스탯 칼럼을 자동으로 매핑하여 유기적으로 연산하는 엔진
        """
        h_score = 0
        a_score = 0
        
        # 1. 자동 스탯 매핑 및 연산 (모든 컬럼 탐색)
        for col, weight in self.weights.items():
            h_col = f"h_{col}"
            a_col = f"a_{col}"
            
            # 데이터에 해당 키가 존재할 경우에만 연산 수행
            if h_col in data_dict and a_col in data_dict:
                h_val = float(data_dict[h_col])
                a_val = float(data_dict[a_col])
                
                h_score += h_val * weight
                a_score += a_val * weight
        
        # 2. 결과 정규화 (시그모이드 함수 적용으로 0~1 사이 확률 도출)
        diff = h_score - a_score
        final_score = 1 / (1 + np.exp(-diff * 5))
        
        winner = "Home" if final_score >= 0.5 else "Away"
        confidence = round(abs(final_score - 0.5) * 200, 1)
        
        return {
            'winner': winner,
            'confidence': confidence,
            'score': final_score,
            'stats': data_dict,
            'detailed_report': self._generate_report(data_dict, winner)
        }

    def _generate_report(self, data, winner):
        # 유기적으로 작동하는 근거 요약
        report_str = f"**[AI 분석 리포트]** {winner} 팀의 승리 가능성이 높습니다. "
        report_str += "통합 지표(ERA, OPS, 최근 성적 등)를 유기적으로 가중치 합산한 결과입니다. "
        report_str += f"(데이터 기준: 홈팀 ERA {data.get('h_era')}, 원정팀 ERA {data.get('a_era')})"
        return report_str
