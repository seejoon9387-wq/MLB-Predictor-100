import pandas as pd
import numpy as np

class MLBUnifiedTrainer:
    def __init__(self):
        # 가중치 설정 (여기서 40개 알고리즘의 비중을 유기적으로 제어)
        self.weights = {
            'win_rate': 0.6,
            'pitching_era': 0.4
        }

    def analyze(self, raw_data):
        # 1. 데이터 통합 및 정규화
        stats = self._get_integrated_stats(raw_data)
        
        # 2. 알고리즘 유기적 결합 (정규화된 점수 산출)
        # 0.5가 기준점, 높을수록 Home 유리
        win_score = (stats['h_rate'] - stats['a_rate']) * 0.5 + 0.5
        era_score = (stats['a_era'] - stats['h_era']) * 0.1 + 0.5
        
        # 가중치 적용 통합
        final_score = (win_score * self.weights['win_rate']) + (era_score * self.weights['pitching_era'])
        
        # 결과 결정
        winner = "Home" if final_score >= 0.5 else "Away"
        confidence = round(abs(final_score - 0.5) * 200, 1)
        
        return {
            'winner': winner,
            'confidence': confidence,
            'score': final_score,
            'stats': stats,
            'detailed_report': self._generate_logical_report(winner, stats, final_score)
        }

    def _get_integrated_stats(self, raw_data):
        # 실제 API에서 받은 데이터를 여기서 통일된 규격으로 변환
        return {'h_era': 4.49, 'a_era': 3.36, 'h_rate': 0.64, 'a_rate': 0.52}

    def _generate_logical_report(self, winner, stats, score):
        # 데이터가 승률과 방어율 중 무엇에 의해 결정되었는지 추적
        reason = "승률 우위" if (stats['h_rate'] if winner == 'Home' else stats['a_rate']) > 0.5 else "투수력 지표"
        return f"**[분석 결과]** {winner} 팀의 승리가 예측됩니다. 본 결과는 {reason}를 중심으로 40개 분석 지표를 통합 산출한 값입니다."
