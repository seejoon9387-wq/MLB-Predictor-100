import pandas as pd
import xgboost as xgb
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from data_loader import load_data
from modules.imputer import fill_missing_values
from modules.outlier import remove_outliers

class MLBPredictionTrainer:
    def __init__(self):
        self.data = load_data()
        self.scaler = StandardScaler()
        self.model = None

    def run_pipeline(self):
        # 1. 정제
        df = fill_missing_values(self.data)
        df = remove_outliers(df)
        
        # 2. 날짜 기준 정렬 (누수 방지 핵심)
        df = df.sort_values('date').reset_index(drop=True)
        
        target = 'is_home_win'
        X = df.drop(columns=[target, 'game_pk', 'date'], errors='ignore')
        y = df[target]
        
        # 3. 80/20 시간순 분리
        split_idx = int(len(df) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        # 4. 스케일링
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # 5. XGBoost 학습
        self.model = xgb.XGBClassifier(
            n_estimators=1000,
            learning_rate=0.01,
            max_depth=6,
            n_jobs=-1,
            early_stopping_rounds=50,
            objective='binary:logistic'
        )
        
        self.model.fit(
            X_train_scaled, y_train,
            eval_set=[(X_test_scaled, y_test)],
            verbose=100
        )
        
        # 6. 평가 및 저장
        print(classification_report(y_test, self.model.predict(X_test_scaled)))
        joblib.dump({'model': self.model, 'scaler': self.scaler}, 'mlb_model.pkl')

if __name__ == "__main__":
    trainer = MLBPredictionTrainer()
    trainer.run_pipeline()
