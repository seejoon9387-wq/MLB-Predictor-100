# main_trainer.py (전체 코드)
from modules.backtester import run_backtest
from modules.inefficiency_engine import detect_market_bias

class MLBUnifiedTrainer:
    def __init__(self, analysis_mode=True):
        self.data = load_data(analysis_mode=analysis_mode)

    def run_full_evaluation(self):
        # 1. 데이터 비효율 분석
        df_analyzed = detect_market_bias(self.data)
        
        # 2. 백테스팅 수행
        report = run_backtest(df_analyzed)
        
        print("--- 백테스팅 결과 보고서 ---")
        for k, v in report.items():
            print(f"{k}: {v}")
            
        return report

if __name__ == "__main__":
    trainer = MLBUnifiedTrainer(analysis_mode=True)
    trainer.run_full_evaluation()
