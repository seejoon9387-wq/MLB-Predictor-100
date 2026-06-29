class MLBUnifiedTrainer:
    def analyze(self, input_data):
        stats = self._get_integrated_stats()
        win_diff = stats['a_rate'] - stats['h_rate']
        era_diff = stats['h_era'] - stats['a_era']
        
        score = 0.5 + (win_diff * 0.6) + (era_diff * 0.05)
        winner = "Home" if score >= 0.5 else "Away"
        confidence = round(abs(score - 0.5) * 200, 1)
        
        return {
            'winner': winner,
            'confidence': confidence,
            'score': score,
            'stats': stats, # 여기서 반환하는 키가 중요합니다
            'detailed_report': self._generate_report(winner, stats, win_diff, era_diff)
        }

    def _get_integrated_stats(self):
        # 모든 키 이름을 app.py와 일치시킴
        return {'h_era': 4.49, 'a_era': 3.36, 'h_rate': 0.64, 'a_rate': 0.52}
        
    def _generate_report(self, winner, stats, win_diff, era_diff):
        if abs(win_diff) > 0.1:
            return f"**[분석 결론]** {winner} 팀의 승리가 예측됩니다. 승률 격차({int(abs(win_diff)*100)}%)가 지배적이었습니다."
        return f"**[분석 결론]** 투수력 격차({abs(era_diff):.2f})로 인해 투수전 양상이 예상됩니다."
