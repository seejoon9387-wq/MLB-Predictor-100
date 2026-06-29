from modules.data_loader import DataLoader
from modules.trainer import Trainer
from modules.optimizer import Optimizer
from modules.registry import Registry

def main_engine_cycle():
    # 1. 데이터 로드 (수백만 건 처리 최적화)
    data = DataLoader.load_historical_data()
    
    # 2. 모델 학습 (Trainer 활용)
    # 수백만 건의 데이터를 배칭(Batching)하여 모델 파라미터 최적화
    model = Trainer.train(data)
    
    # 3. 하이퍼파라미터 튜닝 (Optimizer 활용)
    optimized_model = Optimizer.tune(model, data)
    
    # 4. 결과 레지스트리 저장
    Registry.save_model(optimized_model)
    print("시스템 예측 엔진 최적화 완료.")

if __name__ == "__main__":
    main_engine_cycle()
