from modules.data_loader import load_data # 가공된 데이터를 가져오는 함수
from modules.trainer import Trainer
from modules.optimizer import Optimizer
from modules.registry import Registry
from modules.feature_selector import select_optimal_features

def main_engine_cycle():
    print("🚀 시스템 예측 엔진 학습 시작...")
    
    # 1. 데이터 로드 및 정제 (가공된 피처 셋을 불러옴)
    raw_df = load_data()
    # 최적의 피처만 선택
    refined_df = select_optimal_features(raw_df)
    
    # 2. 모델 학습 (Trainer: 수백만 건 배칭 처리)
    # 데이터프레임을 받아 모델 객체 반환
    model = Trainer.train(refined_df)
    
    # 3. 하이퍼파라미터 튜닝 (Optimizer: 성능 극대화)
    # 70% 이상의 예측 정확도를 위해 모델 구조 최적화
    optimized_model = Optimizer.tune(model, refined_df)
    
    # 4. 결과 레지스트리 저장
    Registry.save_model(optimized_model)
    print("✅ 시스템 예측 엔진 최적화 및 저장 완료.")

if __name__ == "__main__":
    main_engine_cycle()
