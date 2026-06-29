import pandas as pd
import xgboost as xgb
import joblib
from data_loader import load_data
from modules.imputer import fill_missing_values
from modules.outlier import remove_outliers
from modules.feature_selector import remove_collinear_features # 추가

class MLBPredictionTrainer:
    def __init__(self):
        self.data = load_data()
        self.model = None

    def run_pipeline(self):
        # 1. 전처리
        df = fill_missing_values(self.data).sort_values('date').reset_index(drop=True)
        df = remove_outliers(df)
        
        # 2. 다중공선성 제거 (변수 독립성 확보)
        target = 'is_home_win'
        features_df = df.drop(columns=[target, 'game_pk', 'date'], errors='ignore')
        independent_features = remove_collinear_features(features_df, threshold=0.9)
        
        X = df[independent_features.columns]
        y = df[target]
        
        # 3. 시간순 분리 및 학습 (이전 로직 동일)
        split_idx = int(len(df) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        # 4. 최종 학습
        self.model = xgb.XGBClassifier(n_estimators=1000, learning_rate=0.01)
        self.model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=100)
        
        joblib.dump({'model': self.model, 'features': X.columns.tolist()}, 'model_independent.pkl')
        print("독립성이 확보된 모델 저장 완료.")

if __name__ == "__main__":
    trainer = MLBPredictionTrainer()
    trainer.run_pipeline()
