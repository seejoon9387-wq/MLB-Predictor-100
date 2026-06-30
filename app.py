import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split

# 1. 환경 설정 및 데이터 로드
# 현재 프로젝트 폴더(github)에 맞춰 경로 설정
BASE_PATH = r'C:\Users\pc\Desktop\github'
FILE_NAME = 'mlb_master_final.csv'
FILE_PATH = os.path.join(BASE_PATH, FILE_NAME)

def run_mlb_analysis():
    print("--- MLB 분석 엔진 가동 ---")
    
    # 데이터 로드
    if not os.path.exists(FILE_PATH):
        print(f"오류: 파일을 찾을 수 없습니다. 경로 확인: {FILE_PATH}")
        return

    df = pd.read_csv(FILE_PATH)
    
    # 2. 데이터 전처리 (결측치 제거 및 타겟 변수 생성)
    df = df.dropna()
    # 타구 속도 95마일 이상을 안타(1)로 정의
    df['hit_binary'] = (df['launch_speed'] > 95).astype(int)
    
    # 분석에 사용할 피처(Feature) 선택
    features = ['hyper_speed', 'launch_speed_angle', 'release_speed', 'bat_speed']
    X = df[features]
    y = df['hit_binary']
    
    # 3. 데이터 학습/테스트 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. 모델 최적화 (n_estimators=300으로 학습 능력 극대화)
    print("모델 학습 중...")
    model = RandomForestClassifier(
        n_estimators=300, 
        max_depth=20, 
        n_jobs=-1, 
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # 5. 결과 평가
    y_pred = model.predict(X_test)
    
    print("\n[분석 결과]")
    print(f"최종 모델 정확도: {accuracy_score(y_test, y_pred):.4f}")
    print("\n상세 리포트:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    run_mlb_analysis()
