import pandas as pd
from modules.simulator import simulate_match_scenarios

class MLBUnifiedTrainer:
    def __init__(self, data=None):
        self.data = data if data is not None else pd.DataFrame()

    def analyze(self, input_data):
        try:
            if isinstance(input_data, dict):
                game_pk = input_data.get('game_pk', 'Unknown')
                data_for_sim = input_data
            else:
                data_for_sim = input_data.to_dict() if hasattr(input_data, 'to_dict') else input_data
                game_pk = data_for_sim.get('game_pk', 'Unknown')

            sim_result = simulate_match_scenarios(data_for_sim)

            report = {
                'winner': 'Home' if sim_result > 0.5 else 'Away',
                'confidence': round(min(abs(sim_result - 0.5) * 200, 99.9), 1),
                'detailed_report': f"게임 ID {game_pk} 분석 완료. 로직 점수: {sim_result:.2f}"
            }
            return report

        except Exception as e:
            return {'error': str(e), 'status': 'failed'}
