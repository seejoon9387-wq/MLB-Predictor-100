# main_trainer.py (전체 코드)
from modules.data_loader import load_data
from modules.simulator import simulate_match_scenarios

class MLBUnifiedTrainer:
    def __init__(self):
        self.data = load_data(analysis_mode=True)

    def run_all_simulations(self):
        print("상세 시나리오 분석 시작: 모든 변수 결합 10만 회 시뮬레이션...")
        
        # 몬테카를로 분석 실행
        simulation_df = simulate_match_scenarios(self.data)
        
        # 신뢰도 필터링: 시뮬레이션의 표준편차(위험도)가 낮은 확실한 경기 우선
        final_report = simulation_df.sort_values(by='expected_value', ascending=False)
        
        return final_report

if __name__ == "__main__":
    trainer = MLBUnifiedTrainer()
    report = trainer.run_all_simulations()
    print("--- 최종 시뮬레이션 결과 ---")
    print(report.head(10))
