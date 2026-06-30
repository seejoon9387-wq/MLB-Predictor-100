import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# 1. 고속 데이터 로딩
file_path = r'C:\Users\pc\Desktop\github\data\raw\mlb_master_final.csv'
df = pd.read_csv(file_path)

# 2. 결정론적 데이터 정제
essential_cols = ['pitch_type', 'release_speed', 'launch_speed']
df = df.dropna(subset=essential_cols)
df.fillna(0, inplace=True)

# 3. 타겟 설정 (hit_binary: 안타 여부 - 단순화를 위해 launch_speed 기준 예시)
df['hit_binary'] = (df['launch_speed'] > 95).astype(int) 

# 4. 피처 엔지니어링 (상관관계 기반 최적화)
features = ['hyper_speed', 'launch_speed_angle', 'release_speed', 'bat_speed']
X = df[features]
y = df['hit_binary']

# 5. 모델 학습 및 검증 (백테스팅 환경)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42)

print("엔진 학습 시작...")
model.fit(X_train, y_train)

# 6. 결과 도출
y_pred = model.predict(X_test)
print(f"엔진 예측 정확도: {accuracy_score(y_test, y_pred):.4f}")
print("\n[상세 분석 리포트]")
print(classification_report(y_test, y_pred))
