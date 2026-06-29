import pandas as pd
from modules.simulator import simulate_match_scenarios

class MLBUnifiedTrainer:
    def __init__(self, data=None):
        self.data = data if data is not None else pd.DataFrame()

    def analyze(self, input_data):
        try:
            # 기본 데이터 추출
            game_pk = input_data.get('game_pk', 'Unknown')
            
            # 시뮬레이터 실행 (가중치 적용된 점수)
            score = simulate_match_scenarios(input_data)
            
            # 분석 결과 상세화
            winner = "Home" if score >= 0.5 else "Away"
            confidence = round(abs(score - 0.5) * 200, 1)
            
            return {
                'winner': winner,
                'confidence': confidence,
                'score': round(score, 3),
                'detailed_report': (
                    f"분석 결과, {winner}팀의 승리 확률이 {confidence}%로 예측됩니다. "
                    f"(로직 점수: {score:.3f})\n\n"
                    "**[분석 요약]**\n"
                    f"- 현재 베이지안 승률 및 기후 환경 데이터를 종합한 결과입니다.\n"
                    f"- 승패 불확실성이 {100 - confidence}% 존재합니다."
                )
            }
        except Exception as e:
            return {'error': str(e), 'detailed_report': "분석 중 오류 발생"}
