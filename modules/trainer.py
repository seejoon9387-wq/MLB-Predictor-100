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
        df = fill_missing_values(self.data)
        df = remove_outliers(df)
        
        target = 'is_home_win'
        X = df.drop(columns=[target, 'game_pk', 'date'], errors='ignore')
        y = df[target]
        
        # 시계열 분할
        tscv = TimeSeriesSplit(n_splits=5)
        for _, test_idx in tscv.split(X):
            X_train, X_test = X.iloc[:test_idx[0]], X.iloc[test_idx]
            y_train, y_test = y.iloc[:test_idx[0]], y.iloc[test_idx]
            
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # 학습
        self.model = xgb.XGBClassifier(n_estimators=1000, learning_rate=0.03, max_depth=7, n_jobs=-1)
        self.model.fit(X_train_scaled, y_train)
        
        print(classification_report(y_test, self.model.predict(X_test_scaled)))
        joblib.dump({'model': self.model, 'scaler': self.scaler}, 'mlb_model.pkl')

if __name__ == "__main__":
    trainer = MLBPredictionTrainer()
    trainer.run_pipeline()
