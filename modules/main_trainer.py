import joblib
import xgboost as xgb
from data_loader import load_data
from modules.feature_selector import remove_collinear_features
from modules.cv_engine import perform_time_series_cv
from modules.tuner import tune_xgboost
from modules.calibrator import apply_probability_calibration
from modules.residual_analyzer import analyze_residuals

class MLBUnifiedTrainer:
    def __init__(self):
        self.data = load_data()

    def run(self):
        # 1. 데이터 전처리
        df = self.data.sort_values('date').reset_index(drop=True)
        X = remove_collinear_features(df.drop(columns=['is_home_win', 'date', 'game_pk']))
        y = df['is_home_win']
        
        # 2. 시계열 교차 검증을 통한 오버피팅 점검
        base_model = xgb.XGBClassifier(n_jobs=-1)
        perform_time_series_cv(base_model, X, y)
        
        # 3. 하이퍼파라미터 튜닝
        print("하이퍼파라미터 튜닝 시작...")
        split_idx = int(len(df) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        best_params = tune_xgboost(X_train, y_train, X_test, y_test)
        
        # 4. 최종 학습 및 잔차 분석
        final_model = xgb.XGBClassifier(**best_params, n_jobs=-1)
        final_model.fit(X_train, y_train)
        analyze_residuals(y_test, final_model.predict(X_test))
        
        # 5. 확률 교정 및 저장
        calibrated_model = apply_probability_calibration(final_model, X_test, y_test)
        joblib.dump(calibrated_model, 'final_mlb_model_master.pkl')
        print("최종 모델 생성 완료: final_mlb_model_master.pkl")

if __name__ == "__main__":
    MLBUnifiedTrainer().run()
