import joblib
from data_loader import load_data
from modules.tuner import tune_xgboost
from modules.imputer import fill_missing_values

class MLBPredictionTrainer:
    def __init__(self):
        self.data = load_data()

    def run_pipeline(self):
        # 1. 데이터 준비
        df = fill_missing_values(self.data).sort_values('date')
        X = df.drop(columns=['is_home_win', 'game_pk', 'date'], errors='ignore')
        y = df['is_home_win']
        
        # 2. 시간순 분리
        split_idx = int(len(df) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        # 3. 하이퍼파라미터 튜닝 실행
        print("하이퍼파라미터 최적화 시작...")
        best_params = tune_xgboost(X_train, y_train, X_test, y_test)
        print(f"최적 파라미터: {best_params}")
        
        # 4. 최적 파라미터로 최종 학습
        self.model = xgb.XGBClassifier(**best_params, n_estimators=1000, n_jobs=-1)
        self.model.fit(X_train, y_train)
        
        joblib.dump(self.model, 'tuned_model.pkl')
        print("튜닝 완료된 모델 저장 완료.")

if __name__ == "__main__":
    trainer = MLBPredictionTrainer()
    trainer.run_pipeline()
