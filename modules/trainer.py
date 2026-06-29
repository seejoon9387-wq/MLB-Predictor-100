import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from data_loader import load_data

class MLBPredictionTrainer:
    def __init__(self):
        self.data = load_data()
        self.model = None
        self.scaler = StandardScaler()

    def run_pipeline(self):
        # 1. 데이터 준비
        target = 'is_home_win'
        X = self.data.drop(columns=[target, 'game_pk', 'date'])
        X = pd.get_dummies(X) # 범주형 변수 자동 인코딩
        y = self.data[target]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 2. 스케일링
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # 3. 모델 학습
        self.model = xgb.XGBClassifier(n_estimators=500, learning_rate=0.05, max_depth=6, n_jobs=-1)
        self.model.fit(X_train_scaled, y_train)
        
        # 4. 평가
        preds = self.model.predict(X_test_scaled)
        print("최종 모델 성능 평가:")
        print(classification_report(y_test, preds))
        
        # 5. 모델 저장
        joblib.dump({'model': self.model, 'scaler': self.scaler}, 'mlb_model.pkl')
        print("모델 저장 완료: mlb_model.pkl")

if __name__ == "__main__":
    trainer = MLBPredictionTrainer()
    trainer.run_pipeline()
