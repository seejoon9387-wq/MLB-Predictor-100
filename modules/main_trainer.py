import numpy as np

class MLBUnifiedTrainer:
    def __init__(self):
        self.weights = {'era': -0.3, 'ops': 0.4, 'avg': 0.15}

    def analyze(self, data):
        h_score = sum([data.get(f'h_{k}', 0) * v for k, v in self.weights.items()])
        a_score = sum([data.get(f'a_{k}', 0) * v for k, v in self.weights.items()])
        
        final_score = 1 / (1 + np.exp(-(h_score - a_score) * 5))
        
        return {
            "winner": "Home" if final_score >= 0.5 else "Away",
            "confidence": round(abs(final_score - 0.5) * 200, 1),
            "score": final_score
        }
