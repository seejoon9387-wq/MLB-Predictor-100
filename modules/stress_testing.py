import pandas as pd
import numpy as np

class StressTester:
    def __init__(self, model):
        self.model = model

    def run_stress_test(self, data, scenario_name):
        """
        특정 시나리오(부상, 체력 저하 등)를 시뮬레이션하여 모델 성능을 평가합니다.
        """
        print(f"\n[Stress Test 시작: {scenario_name}]")
        
        # 시나리오에 따른 데이터 변형 (예: 강제 노이즈 추가 또는 특정 변수 하향)
        if scenario_name == "Injury_Return":
            data['condition_index'] *= 0.5  # 부상 복귀 직후 컨디션 저하 가정
        elif scenario_name == "Late_Season_Fatigue":
            data['slope_7d'] *= 0.8        # 시즌 후반 모멘텀 하락 가정

        # 모델 예측 및 성능 측정
        predictions = self.model.predict(data.drop(columns=['actual_result']))
        mae = np.mean(np.abs(predictions - data['actual_result']))
        
        print(f"시나리오 '{scenario_name}' 수행 결과 MAE: {mae:.4f}")
        return mae

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    # 더미 모델 및 데이터
    class MockModel:
        def predict(self, x): return np.random.rand(len(x))
    
    mock_data = pd.DataFrame({
        'feature1': np.random.rand(10),
        'condition_index': np.random.rand(10),
        'slope_7d': np.random.rand(10),
        'actual_result': np.random.rand(10)
    })
    
    tester = StressTester(MockModel())
    tester.run_stress_test(mock_data, "Injury_Return")
