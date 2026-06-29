class MLBUnifiedTrainer:
    def analyze(self, input_data):
        stats = self._get_integrated_stats()
        
        # [논리 보정] 홈팀 승률(0.64) - 원정팀 승률(0.52) = +0.12 (Home 유리)
        # 0.5가 기준점이며, 0.5보다 크면 Home, 작으면 Away
        win_diff = stats['h_rate'] - stats['a_rate'] 
        era_diff = stats['a_era'] - stats['h_era'] # 원정 ERA가 낮을수록 원정팀 유리
        
        # 가중치 결합: 승률(70%) + 투수력(30%)
        score = 0.5 + (win_diff * 0.7) + (era_diff * 0.05)
        
        winner = "Home" if score >= 0.5 else "Away"
        confidence = round(abs(score - 0.5) * 200, 1)
        
        return {
            'winner': winner,
            'confidence': confidence,
            'score': score,
            'stats': stats,
            'detailed_report': f"**[분석 결론]** {winner} 팀의 승리가 예측됩니다. (승률 차이: {int(abs(win_diff)*100)}%)"
        }

    def _get_integrated_stats(self):
        return {'h_era': 4.49, 'a_era': 3.36, 'h_rate': 0.64, 'a_rate': 0.52}
