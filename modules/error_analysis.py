import pandas as pd
import matplotlib.pyplot as plt

class ErrorAnalyzer:
    def __init__(self):
        pass

    def analyze_errors(self, df_results):
        """
        예측 오차(Error = Predicted - Actual)를 분석하여 특성별로 시각화
        df_results: 예측값, 실제값, 구장 정보 등이 담긴 데이터프레임
        """
        df_results['error'] = df_results['pred'] - df_results['actual']
        
        # 구장별 평균 오차 분석
        error_by_park = df_results.groupby('park_type')['error'].mean()
        
        print("구장별 평균 오차(음수면 과소평가, 양수면 과대평가):")
        print(error_by_park)
        
        return error_by_park

    def generate_report(self, error_data):
        """오차 분석 리포트 생성"""
        print("\n--- 에러 분석 리포트 ---")
        for park, error in error_data.items():
            print(f"구장 '{park}'에서의 모델 편향: {error:.4f}")

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    df_results = pd.DataFrame({
        'park_type': ['Fenway', 'Yankee', 'Fenway', 'Yankee'],
        'pred': [0.75, 0.80, 0.72, 0.78],
        'actual': [0.70, 0.82, 0.75, 0.76]
    })
    
    analyzer = ErrorAnalyzer()
    error_summary = analyzer.analyze_errors(df_results)
    analyzer.generate_report(error_summary)
