import streamlit as st
import pandas as pd
import requests
import io
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

st.title("MLB 예측 분석 엔진 v1.0")

FILE_ID = "1iSbcXGYzInvd5LQ1jLqdq0MgMtTT09pw"
DATA_URL = f"https://drive.usercontent.google.com/download?id={FILE_ID}&export=download&confirm=t"

# 1. 학습에 꼭 필요한 컬럼만 지정 (메모리 부족 방지)
USE_COLS = ['launch_speed', 'launch_angle', 'bat_speed', 'release_speed', 
            'effective_speed', 'hyper_speed', 'release_extension']

@st.cache_data
def load_data(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    # 필요한 컬럼만 읽어서 메모리 폭발 방지
    df = pd.read_csv(io.BytesIO(response.content), usecols=USE_COLS)
    return df.dropna()

try:
    with st.spinner('마스터 데이터 로딩 및 최적화 중...'):
        df = load_data(DATA_URL)
        
        # 2. 타겟 설정 (95마일 이상 강한 타구 = 1)
        df['hit_binary'] = (df['launch_speed'] > 95).astype(int)
        
        # 3. 피처 선택
        features = ['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension']
        X = df[features]
        y = df['hit_binary']
        
        # 4. 학습
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, max_depth=10, n_jobs=-1)
        model.fit(X_train, y_train)
        
        # 5. 결과
        acc = accuracy_score(y_test, model.predict(X_test))
        
        st.success(f"### 엔진 예측 정확도: {acc:.4f}")
        st.write("학습 데이터 샘플 수:", len(df))
        st.write("사용된 피처:", features)

except Exception as e:
    st.error(f"엔진 가동 오류: {e}")
