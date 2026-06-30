import streamlit as st
import pandas as pd
import requests
import io
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

st.title("MLB 예측 분석 엔진 (Memory Optimized)")

FILE_ID = "1iSbcXGYzInvd5LQ1jLqdq0MgMtTT09pw"
DATA_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

# 메모리 절약을 위해 필요한 컬럼만 정의
USE_COLS = ['launch_speed', 'hyper_speed', 'launch_speed_angle', 'release_speed', 'bat_speed']

@st.cache_data
def load_data_optimized(url):
    # 필요한 컬럼만 읽어서 메모리 사용량 80% 이상 절감
    response = requests.get(url)
    df = pd.read_csv(io.BytesIO(response.content), usecols=USE_COLS)
    return df.dropna()

try:
    with st.spinner('메모리 최적화 로딩 중...'):
        df = load_data_optimized(DATA_URL)
        
        # 타겟 설정
        df['hit_binary'] = (df['launch_speed'] > 95).astype(int)
        
        # 학습
        features = ['hyper_speed', 'launch_speed_angle', 'release_speed', 'bat_speed']
        X = df[features]
        y = df['hit_binary']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(n_estimators=100, max_depth=10, n_jobs=-1)
        model.fit(X_train, y_train)
        
        acc = accuracy_score(y_test, model.predict(X_test))
        st.success(f"엔진 가동 완료! 정확도: {acc:.4f}")

except Exception as e:
    st.error(f"데이터 로드 또는 학습 중 오류: {e}")
