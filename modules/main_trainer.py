import joblib
from data_loader import load_data
from modules.feature_selector import remove_collinear_features
from modules.tuner import tune_xgboost
from modules.calibrator import apply_probability_calibration
from sklearn.model_selection import TimeSeriesSplit

class MLBUnifiedTrainer:
    def __init__(self):
        self.data = load_data()
        self.model = None

    def run(self):
        # 1. 정제 및 다중공선성 제거
        df = self.data.sort_values('date').reset_index(drop=True)
        X = remove_collinear_features(df.drop(columns=['is_home_win', 'date', 'game_pk']))
        y = df['is_home_win']
        
        # 2. 시간순 분리
        split_idx = int(len(df) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        # 3. 튜닝 및 학습
        print("하이퍼파라미터 튜닝 시작...")
        best_params = tune_xgboost(X_train, y_train, X_test, y_test)
        
        print("최종 모델 학습...")
        base_model = xgb.XGBClassifier(**best_params, n_jobs=-1)
        base_model.fit(X_train, y_train)
        
        # 4. 확률 교정 (Calibration)
        print("모델 확률 교정 중...")
        final_model = apply_probability_calibration(base_model, X_test, y_test)
        
        # 5. 저장
        joblib.dump(final_model, 'final_mlb_model_v1.pkl')
        print("학습 및 교정 완료: final_mlb_model_v1.pkl")

if __name__ == "__main__":
    trainer = MLBUnifiedTrainer()
    trainer.run()
