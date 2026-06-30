import pandas as pd
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import numpy as np

def run_mlb_engine(file_path):
    print("--- 1단계: 대용량 데이터 로딩 및 전처리 시작 ---")
    cols = ['pitch_type', 'release_speed', 'release_spin_rate', 'balls', 'strikes', 
            'on_1b', 'on_2b', 'on_3b', 'outs_when_up', 'home_score_diff', 'stand', 'p_throws', 'woba_value']
    
    df = pd.read_csv(file_path, usecols=cols)
    df = df.dropna(subset=['woba_value'])
    df = df.fillna(0)
    
    for col in ['pitch_type', 'stand', 'p_throws']:
        df[col] = df[col].astype(str)
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
    
    print("--- 2단계: 시계열 검증 기반 학습 준비 ---")
    X = df.drop(columns=['woba_value'])
    y = df['woba_value']
    
    # 모델 정의
    model = xgb.XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        tree_method='hist' # 대용량 데이터 학습 가속화
    )
    
    # Time-Series Split (과거 데이터로 미래 예측)
    tscv = TimeSeriesSplit(n_splits=3)
    
    print("--- 3단계: 전체 데이터 학습 및 평가 수행 ---")
    for fold, (train_index, test_index) in enumerate(tscv.split(X)):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        print(f"Fold {fold+1} 완료 | RMSE: {rmse:.4f}")
        
    print("--- 완료: 예측 엔진 학습 및 검증 완료 ---")
    return model

if __name__ == "__main__":
    path = r'C:\Users\pc\Desktop\github\mlb_master_final.csv'
    model = run_mlb_engine(path)
    # 모델 저장 (차후 사용)
    model.save_model("mlb_predict_engine.json")
    print("엔진 모델 파일(mlb_predict_engine.json)이 생성되었습니다.")
