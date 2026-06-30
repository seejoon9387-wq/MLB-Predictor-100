import pandas as pd

class BacktestingEngine:
    def __init__(self, model):
        self.model = model

    def run_simulation(self, historical_data):
        """
        과거 데이터를 순차적으로 입력하여 예측 시뮬레이션 수행
        historical_data는 날짜순으로 정렬된 데이터프레임이어야 함
        """
        results = []
        # 시간 순서대로 데이터를 슬라이딩하며 예측 수행
        for i in range(len(historical_data) - 1):
            train_set = historical_data.iloc[:i+1]
            test_target = historical_data.iloc[i+1:i+2]
            
            # 예측 수행
            pred = self.model.predict(test_target)
            actual = test_target['actual_result'].values[0]
            
            results.append({'pred': pred[0], 'actual': actual})
            
        return pd.DataFrame(results)

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    # 과거 경기 데이터 시뮬레이션 데이터
    hist_data = pd.DataFrame({
        'feature1': [0.5, 0.6, 0.7],
        'actual_result': [1, 0, 1]
    })
    
    # 더미 모델 (predict 메서드 필요)
    class DummyModel:
        def predict(self, x): return [1]
        
    engine = BacktestingEngine(DummyModel())
    backtest_results = engine.run_simulation(hist_data)
    
    print("백테스팅 시뮬레이션 결과(일부):")
    print(backtest_results.head())
