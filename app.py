import pandas as pd
import subprocess
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split

# 설정
FILE_PATH = r'C:\Users\pc\Desktop\github\data\raw\mlb_master_final.csv'
GIT_DIR = r'C:\Users\pc\Desktop\github\data\raw'

def run_engine():
    print("--- 1. 데이터 분석 및 모델 학습 시작 ---")
    
    # 데이터 로드 및 정제
    df = pd.read_csv(FILE_PATH, usecols=['launch_speed', 'hyper_speed', 'launch_speed_angle', 'release_speed', 'bat_speed'])
    df = df.dropna()
    df['hit_binary'] = (df['launch_speed'] > 95).astype(int)
    
    X = df[['hyper_speed', 'launch_speed_angle', 'release_speed', 'bat_speed']]
    y = df['hit_binary']
    
    # 학습
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=50, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # 결과 출력
    y_pred = model.predict(X_test)
    print(f"모델 정확도: {accuracy_score(y_test, y_pred):.4f}")
    
    print("--- 2. Git 자동 연동 시도 ---")
    try:
        # Git이 설치된 경로를 직접 지정하거나, 시스템 Path를 통해 호출
        os.chdir(GIT_DIR)
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', 'app.py'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Auto-update engine results'], check=True)
        print("Git 연동 및 커밋 성공.")
    except Exception as e:
        print(f"Git 자동 실행 실패: {e}. (수동으로 git add . 명령을 사용하세요)")

if __name__ == "__main__":
    run_engine()
