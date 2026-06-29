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
    def __init__(self):
        self.data = load_data()
        self.model = None
        self.X_train, self.y_train = None, None

    def run(self):
        try:
            df = self.data.sort_values('date').reset_index(drop=True)
            X = remove_collinear_features(df.drop(columns=['is_home_win', 'date', 'game_pk']))
            y = df['is_home_win']
            
            split_idx = int(len(df) * 0.8)
            self.X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
            self.y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
            
            logger.info("학습 파이프라인 시작")
            best_params = tune_xgboost(self.X_train, self.y_train, X_test, y_test)
            
            self.model = xgb.XGBClassifier(**best_params, n_jobs=-1)
            self.model.fit(self.X_train, self.y_train)
            
            # 자가 진화 실행
            evolution = SelfEvolvingLoop(self)
            evolution.run_evolution_cycle()
            
            logger.info("모든 프로세스 완료")
        except Exception as e:
            logger.error(f"시스템 오류: {str(e)}", exc_info=True)

if __name__ == "__main__":
    MLBUnifiedTrainer().run()
