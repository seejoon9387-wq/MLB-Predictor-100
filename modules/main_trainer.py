import joblib
import xgboost as xgb
from data_loader import load_data
from modules.feature_selector import remove_collinear_features
from modules.cv_engine import perform_time_series_cv
from modules.tuner import tune_xgboost
from modules.calibrator import apply_probability_calibration
from modules.residual_analyzer import analyze_residuals
from modules.logger import get_logger

logger = get_logger("MLB_Trainer")

class MLBUnifiedTrainer:
    def __init__(self):
        logger.info("시스템 초기화: 데이터 로딩 시작")
        self.data = load_data()

    def run(self):
        try:
            # 1. 전처리 및 독립성 확보
            df = self.data.sort_values('date').reset_index(drop=True)
            X = remove_collinear_features(df.drop(columns=['is_home_win', 'date', 'game_pk']))
            y = df['is_home_win']
            logger.info(f"데이터 정제 완료: {X.shape[1]}개의 독립 피처 사용")

            # 2. 교차 검증 (과적합 방지)
            logger.info("시계열 교차 검증 시작")
            perform_time_series_cv(xgb.XGBClassifier(), X, y)

            # 3. 하이퍼파라미터 튜닝
            split_idx = int(len(df) * 0.8)
            X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
            y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
            
            logger.info("하이퍼파라미터 최적화(Optuna) 실행")
            best_params = tune_xgboost(X_train, y_train, X_test, y_test)

            # 4. 최종 모델 학습 및 잔차 분석
            final_model = xgb.XGBClassifier(**best_params, n_jobs=-1)
            final_model.fit(X_train, y_train)
            analyze_residuals(y_test, final_model.predict(X_test))
            
            # 5. 확률 교정 및 저장
            calibrated_model = apply_probability_calibration(final_model, X_test, y_test)
            joblib.dump(calibrated_model, 'final_mlb_model_master.pkl')
            logger.info("학습 및 배포 파이프라인 성공적으로 종료")
            
        except Exception as e:
            logger.error(f"파이프라인 치명적 오류: {str(e)}", exc_info=True)

if __name__ == "__main__":
    MLBUnifiedTrainer().run()
