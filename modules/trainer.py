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
        self.final_features = None

    def run_pipeline(self):
        # 1. 데이터 정제
        df = fill_missing_values(self.data).sort_values('date').reset_index(drop=True)
        df = remove_outliers(df)
        
        target = 'is_home_win'
        X = df.drop(columns=[target, 'game_pk', 'date'], errors='ignore')
        y = df[target]
        
        # 2. 시간순 분할 (Train/Test)
        split_idx = int(len(df) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        # 3. 1차 학습 (중요도 측정용)
        model_temp = xgb.XGBClassifier(n_estimators=500, n_jobs=-1).fit(X_train, y_train)
        
        # 4. 중요도 기반 변수 필터링
        feat_imp = pd.DataFrame({'f': X.columns, 'i': model_temp.feature_importances_})
        self.final_features = feat_imp[feat_imp['i'] > feat_imp['i'].quantile(0.2)]['f'].tolist()
        
        # 5. 최종 모델 학습 (선별된 변수만 활용)
        X_train_final = X_train[self.final_features]
        X_test_final = X_test[self.final_features]
        
        self.model = xgb.XGBClassifier(
            n_estimators=1000, learning_rate=0.01, max_depth=6,
            early_stopping_rounds=50, objective='binary:logistic'
        )
        self.model.fit(X_train_final, y_train, eval_set=[(X_test_final, y_test)], verbose=100)
        
        # 6. 저장
        joblib.dump({'model': self.model, 'features': self.final_features}, 'mlb_model.pkl')
        print(f"최종 모델 저장 완료. 활용 피처 수: {len(self.final_features)}")

if __name__ == "__main__":
    trainer = MLBPredictionTrainer()
    trainer.run_pipeline()
