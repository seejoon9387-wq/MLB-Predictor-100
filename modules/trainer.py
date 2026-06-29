import pandas as pd
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from data_loader import load_data
from modules.imputer import fill_missing_values
from modules.outlier import remove_outliers

class MLBPredictionTrainer:
    def __init__(self):
        """데이터를 로드하고 학습 준비를 수행합니다."""
        print("데이터 로딩 및 피처 엔진 통합 시작...")
        self.data = load_data()
        self.scaler = StandardScaler()
        self.model = None

    def run_pipeline(self):
        # 1. 데이터 정제 (결측치/이상치 처리)
        df = fill_missing_values(self.data)
        df = remove_outliers(df)
        
        # 2. 타깃 및 피처 분리
        target = 'is_home_win'
        # 모델 학습에 불필요한 메타 데이터 제외
        X = df.drop(columns=[target, 'game_pk', 'date'], errors='ignore')
        y = df[target]
        
        # 3. 시계열 학습 분할 (과거 데이터를 학습하여 미래 예측)
        tscv = TimeSeriesSplit(n_splits=5)
        
        X_train, X_test, y_train, y_test = None, None, None, None
        for _, test_idx in tscv.split(X):
            X_train, X_test = X.iloc[:test_idx[0]], X.iloc[test_idx]
            y_train, y_test = y.iloc[:test_idx[0]], y.iloc[test_idx]
            
        # 4. 피처 스케일링
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # 5. XGBoost 모델 정의 및 학습
        # 승패 예측은 이진 분류이므로 binary:logistic 사용
        self.model = xgb.XGBClassifier(
            n_estimators=1000,
            learning_rate=0.03,
            max_depth=7,
            subsample=0.8,
            colsample_bytree=0.8,
            n_jobs=-1,
            early_stopping_rounds=50,
            objective='binary:logistic'
        )
        
        print("모델 학습 시작...")
        self.model.fit(
            X_train_scaled, y_train,
            eval_set=[(X_test_scaled, y_test)],
            verbose=100
        )
        
        # 6. 최종 성능 평가
        preds = self.model.predict(X_test_scaled)
        print("\n=== 최종 모델 성능 보고서 ===")
        print(f"Accuracy: {accuracy_score(y_test, preds):.4f}")
        print(classification_report(y_test, preds))
        
        # 7. 모델 및 스케일러 저장 (추후 예측 서비스에서 사용)
        joblib.dump({'model': self.model, 'scaler': self.scaler}, 'mlb_model.pkl')
        print("\n모델 저장 완료: mlb_model.pkl")
        
        # 8. 피처 중요도 시각화 (선택 사항)
        self.plot_feature_importance(X.columns)

    def plot_feature_importance(self, feature_names):
        """어떤 변수가 승패 예측에 가장 큰 기여를 했는지 확인"""
        importance = self.model.feature_importances_
        feat_importances = pd.Series(importance, index=feature_names)
        feat_importances.nlargest(20).plot(kind='barh', figsize=(10, 8))
        plt.title("Top 20 Important Features")
        plt.show()

if __name__ == "__main__":
    trainer = MLBPredictionTrainer()
    trainer.run_pipeline()
