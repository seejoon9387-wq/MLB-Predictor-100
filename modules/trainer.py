import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import TimeSeriesSplit
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
        # 1. 결측치 및 아웃라이어 처리
        df = fill_missing_values(self.data)
        df = remove_outliers(df)
        
        # 2. 피처/타깃 분리
        target = 'is_home_win'
        X = df.drop(columns=[target, 'game_pk', 'date'], errors='ignore')
        y = df[target]
        
        # 3. 시계열 학습 분할 (Time Series Split)
        tscv = TimeSeriesSplit(n_splits=5)
        X_train, X_test, y_train, y_test = None, None, None, None
        
        for train_idx, test_idx in tscv.split(X):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            
        # 4. 스케일링
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # 5. XGBoost 학습
        self.model = xgb.XGBClassifier(
            n_estimators=1000,
            learning_rate=0.03,
            max_depth=7,
            subsample=0.8,
            colsample_bytree=0.8,
            n_jobs=-1,
            early_stopping_rounds=50
        )
        
        self.model.fit(
            X_train_scaled, y_train,
            eval_set=[(X_test_scaled, y_test)],
            verbose=100
        )
        
        # 6. 결과 평가 및 모델 저장
        print("최종 모델 평가:")
        print(classification_report(y_test, self.model.predict(X_test_scaled)))
        
        joblib.dump({'model': self.model, 'scaler': self.scaler}, 'mlb_model.pkl')
        print("모델 저장 완료: mlb_model.pkl")

if __name__ == "__main__":
    trainer = MLBPredictionTrainer()
    trainer.run_pipeline()
