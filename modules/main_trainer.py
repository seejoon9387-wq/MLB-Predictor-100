# main_trainer.py (전체 코드)
from modules.data_loader import load_data
from modules.simulator import simulate_match_scenarios
from modules.briefing_engine import generate_match_briefing

class MLBUnifiedTrainer:
    def __init__(self):
        self.data = load_data(analysis_mode=True)
        # 모든 알고리즘을 결합한 데이터셋 구축
        self.simulated_data = simulate_match_scenarios(self.data)
        self.data = self.data.merge(self.simulated_data, on='game_pk')

    def get_briefing(self, game_pk):
        if game_pk not in self.data['game_pk'].values:
            return "해당 경기 ID를 찾을 수 없습니다."
        return generate_match_briefing(game_pk, self.data)

if __name__ == "__main__":
    trainer = MLBUnifiedTrainer()
    target_pk = 718000 # 분석하고 싶은 경기 ID 입력
    print(trainer.get_briefing(target_pk))
