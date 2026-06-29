class MLBUnifiedTrainer:
    def analyze(self, input_data):
        # 1. 데이터 통합: 모든 지표를 여기서 수집
        stats = self._get_integrated_stats()
        
        # 2. 우선순위 기반 가중치 계산 (유기적 로직)
        win_diff = stats['a_rate'] - stats['h_rate']  # 승률 차이
        era_diff = stats['h_era'] - stats['a_era']    # 방어율 차이 (낮을수록 유리)
        
        # 승률 차이(60%)와 투수력 차이(40%)를 결합하여 최종 점수 산출
        score = 0.5 + (win_diff * 0.6) + (era_diff * 0.05)
        
        # 3. 결과 결정 및 리포트 생성
        winner = "Home" if score >= 0.5 else "Away"
        confidence = round(abs(score - 0.5) * 200, 1)
        
        return {
            'winner': winner,
            'confidence': confidence,
            'score': score,
            'stats': stats,
            'detailed_report': self._generate_report(winner, stats, win_diff, era_diff)
        }

    def _get_integrated_stats(self):
        # 40여 개 모듈이 수집한 데이터를 반환한다고 가정
        return {'h_era': 4.49, 'a_era': 3.36, 'h_rate': 0.64, 'a_rate': 0.52}

    def _generate_report(self, winner, stats, win_diff, era_diff):
        # 로직: 승률이 10% 이상 차이나면 승률이 지배적이라고 판단
        if abs(win_diff) > 0.1:
            return f"**[분석 결론]** {winner} 팀의 승리가 예측됩니다. 승률 격차({int(abs(win_diff)*100)}%)가 투수력 차이보다 지배적인 변수로 작용했습니다."
        return f"**[분석 결론]** 투수력 격차({abs(era_diff):.2f})가 승률 차이를 상쇄하여 투수전 양상이 예상됩니다."
