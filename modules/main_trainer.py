import numpy as np

class MLBUnifiedTrainer:
    def __init__(self):
        # 데이터 키와 일치하는 가중치 사전
        self.weights = {
            'era': -0.3, 'ops': 0.4, 'last_10': 0.2, 'whip': -0.15, 'avg': 0.15
        }

    def analyze(self, data_dict):
        h_score, a_score = 0, 0
        
        for col, weight in self.weights.items():
            h_col, a_col = f"h_{col}", f"a_{col}"
            if h_col in data_dict and a_col in data_dict:
                h_score += float(data_dict[h_col]) * weight
                a_score += float(data_dict[a_col]) * weight
        
        final_score = 1 / (1 + np.exp(-(h_score - a_score) * 5))
        winner = "Home" if final_score >= 0.5 else "Away"
        confidence = round(abs(final_score - 0.5) * 200, 1)
        
        return {
            'winner': winner,
            'confidence': confidence,
            'score': final_score,
            'stats': data_dict, # 입력된 데이터를 그대로 반환
            'detailed_report': f"{winner} 팀의 우세가 예측됩니다."
        }
