import pandas as pd
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from data_loader import load_data
from modules.imputer import fill_missing_values
from modules.outlier import remove_outliers

class MLBPredictionTrainer:
    def __init__(self):
        self.data = load_data()
        self.model = None
        self.scaler = StandardScaler()

    def run_pipeline(self):
        # 1. 전처리 파이프라인
        df = fill_missing_values(self.data)
        df = remove_outliers(df)
        
        target = 'is_home_win'
        X = df.drop(columns=[target, 'game_pk', 'date'])
        y = df[target]
        
        # 2. 시계열 분할 학습
        tscv = TimeSeriesSplit(n_splits=5)
        for train_idx, test_idx in tscv.split(X):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            
        # 3. 스케일링 및 모델 학습
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model = xgb.XGBClassifier(
            n_estimators=1000,
            learning_rate=0.03,
            max_depth=7,
            n_jobs=-1,
            early_stopping_rounds=50
        )
        self.model.fit(
            X_train_scaled, y_train,
            eval_set=[(X_test_scaled, y_test)],
            verbose=False
        )
        
        # 4. 결과 출력
        print("최종 모델 학습 완료.")
        print(classification_report(y_test, self.model.predict(X_test_scaled)))
        
        # 5. 모델/스케일러 저장
        joblib.dump({'model': self.model, 'scaler': self.scaler}, 'mlb_model.pkl')

if __name__ == "__main__":
    trainer = MLBPredictionTrainer()
    trainer.run_pipeline()
