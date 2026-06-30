import streamlit as st
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

st.title("MLB 예측 분석 엔진")

# 파일 경로: 저장소 최상위에 파일이 있다고 가정
FILE_NAME = 'mlb_master_final.csv'

if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    df = df.dropna()
    
    # 95마일 이상을 안타(1)로 정의
    df['hit_binary'] = (df['launch_speed'] > 95).astype(int)
    
    # 분석 피처 설정
    features = ['hyper_speed', 'launch_speed_angle', 'release_speed', 'bat_speed']
    X = df[features]
    y = df['hit_binary']
    
    # 학습 및 평가
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=300, max_depth=20, n_jobs=-1, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    st.success(f"현재 엔진 예측 정확도: {accuracy:.4f}")
    st.write("모델 학습이 성공적으로 완료되었습니다.")
else:
    st.error(f"파일을 찾을 수 없습니다: {FILE_NAME}. 저장소에 파일이 있는지 확인하세요.")
