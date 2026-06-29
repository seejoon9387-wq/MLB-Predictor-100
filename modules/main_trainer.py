import numpy as np

class MLBUnifiedTrainer:
    def __init__(self):
        # 40개 알고리즘 가중치 관리 (키값은 데이터 딕셔너리의 접미사와 동일해야 함)
        self.weights = {
            'era': -0.3, 'ops': 0.4, 'last_10': 0.2, 'whip': -0.15, 'avg': 0.15
        }

    def analyze(self, data_dict):
        h_score, a_score = 0, 0
        
        # 데이터에 있는 키를 기반으로 자동 연산
        for col, weight in self.weights.items():
            h_key, a_key = f"h_{col}", f"a_{col}"
            # 데이터 존재 여부 확인 후 계산
            if h_key in data_dict and a_key in data_dict:
                h_score += float(data_dict[h_key]) * weight
                a_score += float(data_dict[a_key]) * weight
        
        # 확률 도출 (시그모이드)
        final_score = 1 / (1 + np.exp(-(h_score - a_score) * 5))
        
        return {
            'winner': "Home" if final_score >= 0.5 else "Away",
            'confidence': round(abs(final_score - 0.5) * 200, 1),
            'score': final_score,
            'stats': data_dict
        }
