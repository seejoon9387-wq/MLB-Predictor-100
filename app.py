import pandas as pd
import subprocess
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split

# 설정
FILE_PATH = r'C:\Users\pc\Desktop\github\data\raw\mlb_master_final.csv'
GIT_EXE = r'C:\Program Files\Git\bin\git.exe'
GIT_DIR = r'C:\Users\pc\Desktop\github\data\raw'

def run_engine():
    print("--- 1. 데이터 분석 및 모델 학습 시작 ---")
    
    # 데이터 로드
    try:
        df = pd.read_csv(FILE_PATH, usecols=['launch_speed', 'hyper_speed', 'launch_speed_angle', 'release_speed', 'bat_speed'])
        df = df.dropna()
        df['hit_binary'] = (df['launch_speed'] > 95).astype(int)
        
        X = df[['hyper_speed', 'launch_speed_angle', 'release_speed', 'bat_speed']]
        y = df['hit_binary']
        
        # 학습
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        model = RandomForestClassifier(n_estimators=50, n_jobs=-1)
        model.fit(X_train, y_train)
        
        # 결과
        y_pred = model.predict(X_test)
        print(f"모델 정확도: {accuracy_score(y_test, y_pred):.4f}")
        print(classification_report(y_test, y_pred))
        
    except Exception as e:
        print(f"분석 단계 오류: {e}")
        return

    print("--- 2. Git 연동 시작 ---")
    try:
        os.chdir(GIT_DIR)
        # Git 명령 직접 호출
        subprocess.run([GIT_EXE, 'init'], check=True)
        subprocess.run([GIT_EXE, 'add', '.'], check=True)
        subprocess.run([GIT_EXE, 'commit', '-m', 'Automated engine update'], check=True)
        print("Git 작업 완료 (init, add, commit).")
    except Exception as e:
        print(f"Git 실행 오류: {e}")

if __name__ == "__main__":
    run_engine()
    input("\n모든 작업이 완료되었습니다. Enter를 누르면 종료됩니다.")
