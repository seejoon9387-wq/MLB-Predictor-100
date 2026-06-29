import joblib
import xgboost as xgb
from data_loader import load_data
from modules.feature_selector import remove_collinear_features
from modules.cv_engine import perform_time_series_cv
from modules.tuner import tune_xgboost
from modules.calibrator import apply_probability_calibration
from modules.residual_analyzer import analyze_residuals
from modules.logger import get_logger
from modules.evolution import SelfEvolvingLoop

logger = get_logger("MLB_Master_System")

class MLBUnifiedTrainer:
    def __init__(self, analysis_mode=False):
        # 호출 시 인자 전달
        logger.info(f"시스템 초기화: analysis_mode={analysis_mode}")
        self.data = load_data(analysis_mode=analysis_mode)
        self.model = None
        self.X_train, self.y_train = None, None

    def run(self):
        try:
            if self.data.empty:
                logger.error("데이터 로드 실패: 파일을 확인하세요.")
                return

            df = self.data.sort_values('date').reset_index(drop=True)
            X = remove_collinear_features(df.drop(columns=['is_home_win', 'date', 'game_pk'], errors='ignore'))
            y = df['is_home_win']
            
            # 시간 기반 분할
            split_idx = int(len(df) * 0.8)
            self.X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
            self.y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
            
            logger.info("최적화 및 학습 파이프라인 시작")
            best_params = tune_xgboost(self.X_train, self.y_train, X_test, y_test)
            
            self.model = xgb.XGBClassifier(**best_params, n_jobs=-1)
            self.model.fit(self.X_train, self.y_train)
            
            # 자가 진화 루프 실행
            evolution = SelfEvolvingLoop(self)
            evolution.run_evolution_cycle()
            
            logger.info("파이프라인 정상 종료")
            
        except Exception as e:
            logger.error(f"시스템 오류 발생: {str(e)}", exc_info=True)

if __name__ == "__main__":
    # 실행 시 analysis_mode 설정 (기본값 False)
    trainer = MLBUnifiedTrainer(analysis_mode=True)
    trainer.run()
