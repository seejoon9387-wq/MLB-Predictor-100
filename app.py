import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import sys

# 1. 고정 경로 설정 및 데이터 로딩 (메모리 최적화)
FILE_PATH = r'C:\Users\pc\Desktop\github\data\raw\mlb_master_final.csv'

def run_engine():
    print("--- 엔진 프로세스 시작 ---")
    
    # 필수 컬럼만 로드하여 메모리 절약
    cols = ['launch_speed', 'hyper_speed', 'launch_speed_angle', 'release_speed', 'bat_speed']
    try:
        df = pd.read_csv(FILE_PATH, usecols=lambda c: c in cols or c == 'launch_speed')
    except Exception as e:
        print(f"데이터 로드 오류: {e}")
        return

    # 2. 데이터 정제
    df = df.dropna()
    df['hit_binary'] = (df['launch_speed'] > 95).astype(int)
    
    # 3. 모델링 데이터 준비
    features = ['hyper_speed', 'launch_speed_angle', 'release_speed', 'bat_speed']
    X = df[features]
    y = df['hit_binary']
    
    # 4. 학습 (데이터가 크므로 부분 샘플링 학습)
    print("모델 학습 중...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    model = RandomForestClassifier(n_estimators=50, max_depth=10, n_jobs=-1, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. 결과 도출 및 출력
    y_pred = model.predict(X_test)
    
    print("\n" + "="*30)
    print("분석 엔진 학습 완료")
    print(f"모델 정확도: {accuracy_score(y_test, y_pred):.4f}")
    print("\n상세 분석 리포트:")
    print(classification_report(y_test, y_pred))
    print("="*30)

if __name__ == "__main__":
    run_engine()
    input("\n작업이 완료되었습니다. Enter를 누르면 종료됩니다.")
