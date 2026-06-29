import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from data_loader import load_data
from modules.imputer import fill_missing_values
from modules.feature_selector import remove_collinear_features

def run_baseline_model():
    # 1. 데이터 로드 및 전처리
    data = load_data()
    df = fill_missing_values(data).sort_values('date').reset_index(drop=True)
    
    # 2. 독립 피처 확보 (이미 선별된 피처 사용)
    target = 'is_home_win'
    X = df.drop(columns=[target, 'game_pk', 'date'], errors='ignore')
    y = df[target]
    
    # 3. 시간순 분리
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    # 4. 스케일링 (로지스틱 회귀는 스케일링이 필수)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 5. 로지스틱 회귀 학습 (Baseline)
    log_reg = LogisticRegression(solver='liblinear')
    log_reg.fit(X_train_scaled, y_train)
    
    # 6. 결과 출력
    preds = log_reg.predict(X_test_scaled)
    print("\n=== Logistic Regression (Baseline) Performance ===")
    print(f"Accuracy: {accuracy_score(y_test, preds):.4f}")
    print(classification_report(y_test, preds))

if __name__ == "__main__":
    run_baseline_model()
