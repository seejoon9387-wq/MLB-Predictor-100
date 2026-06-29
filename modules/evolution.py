import joblib
from modules.logger import get_logger

logger = get_logger("Self_Evolving_AI")

class SelfEvolvingLoop:
    def __init__(self, trainer):
        self.trainer = trainer

    def run_evolution_cycle(self):
        logger.info("자가 진화 루프 시작: 피드백 데이터 수집")
        # 최근 학습된 모델로 현재 데이터 예측
        current_data = self.trainer.data 
        y_true = current_data['is_home_win']
        y_pred = self.trainer.model.predict(current_data.drop(columns=['is_home_win', 'date', 'game_pk'], errors='ignore'))
        
        error_mask = (y_true != y_pred)
        
        logger.info("모델 전략 수정: 실패 패턴 데이터 가중치 상향")
        weights = [2.0 if m else 1.0 for m in error_mask]
        
        logger.info("자동 재학습 수행")
        self.trainer.model.fit(self.trainer.X_train, self.trainer.y_train, sample_weight=weights)
        
        joblib.dump(self.trainer.model, 'evolved_model_v_latest.pkl')
        logger.info("진화 완료: 모델 버전 업데이트")
