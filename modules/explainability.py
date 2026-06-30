import shap
import matplotlib.pyplot as plt

class XAIExplainer:
    def __init__(self, model):
        # 모델에 맞는 SHAP Explainer 생성
        self.explainer = shap.Explainer(model)

    def explain_prediction(self, X_sample):
        """
        특정 데이터 샘플에 대한 예측 기여도를 분석합니다.
        """
        shap_values = self.explainer(X_sample)
        
        # 기여도 요약 시각화
        shap.plots.waterfall(shap_values[0], show=False)
        plt.title("예측 기여도 분석 (SHAP Waterfall)")
        plt.show()
        
        return shap_values

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    # 예시를 위해 더미 설명기 생성 (실제 모델 객체 전달 필요)
    print("XAI 모듈 초기화 완료: SHAP을 통한 예측 근거 추적 준비.")
