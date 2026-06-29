import numpy as np

class MLBUnifiedTrainer:
    def __init__(self):
        self.weights = {
            'era': -0.3, 'ops': 0.4, 'last_10': 0.2, 
            'whip': -0.15, 'avg': 0.15, 'win_rate': 0.5
        }

    def analyze(self, data_dict):
        h_score, a_score = 0, 0
        for col, weight in self.weights.items():
            h_key, a_key = f"h_{col}", f"a_{col}"
            if h_key in data_dict and a_key in data_dict:
                h_score += float(data_dict[h_key]) * weight
                a_score += float(data_dict[a_key]) * weight
        
        final_score = 1 / (1 + np.exp(-(h_score - a_score) * 5))
        return {
            "winner": "Home" if final_score >= 0.5 else "Away",
            "confidence": round(abs(final_score - 0.5) * 200, 1),
            "score": final_score,
            "stats": data_dict
        }
