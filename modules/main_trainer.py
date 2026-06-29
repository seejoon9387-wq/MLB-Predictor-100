import joblib
import xgboost as xgb
from data_loader import load_data
from modules.feature_selector import remove_collinear_features
from modules.cv_engine import perform_time_series_cv
from modules.tuner import tune_xgboost
from modules.calibrator import apply_probability_calibration
from modules.residual_analyzer import analyze_residuals
from modules.logger import get_logger

logger = get_logger("MLB_Master_System")

class MLBUnifiedTrainer:
    def __init__(self):
        logger.info("시스템 시작: 데이터 로딩 및 시장 정보 통합")
        self.data = load_data()

    def run(self):
        try:
            # 1. 데이터 전처리 및 독립성 확보
            df = self.data.sort_values('date').reset_index(drop=True)
            X = remove_collinear_features(df.drop(columns=['is_home_win', 'date', 'game_pk']))
            y = df['is_home_win']
            logger.info(f"데이터 준비 완료: {X.shape[1]}개의 피처 활용")

            # 2. 교차 검증 (시계열 데이터 보호)
            logger.info("시계열 교차 검증 수행 중")
            perform_time_series_cv(xgb.XGBClassifier(), X, y)

            # 3. 튜닝 및 학습
            split_idx = int(len(df) * 0.8)
            X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
            y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
            
            logger.info("하이퍼파라미터 최적화 시작")
            best_params = tune_xgboost(X_train, y_train, X_test, y_test)
            
            final_model = xgb.XGBClassifier(**best_params, n_jobs=-1)
            final_model.fit(X_train, y_train)
            
            # 4. 분석 및 교정
            analyze_residuals(y_test, final_model.predict(X_test))
            calibrated_model = apply_probability_calibration(final_model, X_test, y_test)
            
            # 5. 저장
            joblib.dump(calibrated_model, 'final_mlb_model_master.pkl')
            logger.info("파이프라인 완료: 모델 저장 완료")
            
        except Exception as e:
            logger.error(f"운영 오류 발생: {str(e)}", exc_info=True)

if __name__ == "__main__":
    MLBUnifiedTrainer().run()
