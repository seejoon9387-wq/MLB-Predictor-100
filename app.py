import streamlit as st
import pandas as pd
import requests
import io
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

st.title("MLB 예측 분석 엔진 (Master Engine)")

# 구글 드라이브에서 직접 다운로드 가능한 URL로 변환
FILE_ID = "1iSbcXGYzInvd5LQ1jLqdq0MgMtTT09pw"
DATA_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

@st.cache_data
def load_data(url):
    with st.spinner('구글 드라이브에서 대용량 데이터를 불러오는 중...'):
        response = requests.get(url)
        content = io.BytesIO(response.content)
        return pd.read_csv(content)

try:
    # 1. 데이터 로드
    df = load_data(DATA_URL)
    df = df.dropna()
    
    # 2. 타겟 변수 생성 (95마일 이상 안타)
    df['hit_binary'] = (df['launch_speed'] > 95).astype(int)
    
    # 3. 모델 학습 피처 설정
    features = ['hyper_speed', 'launch_speed_angle', 'release_speed', 'bat_speed']
    X = df[features]
    y = df['hit_binary']
    
    # 4. 학습/테스트 분리 및 모델 가동
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=300, max_depth=20, n_jobs=-1, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. 결과 산출
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    st.success(f"### 엔진 예측 정확도: {accuracy:.4f}")
    st.write("---")
    st.write("데이터가 성공적으로 마스터 엔진에 통합되어 학습되었습니다.")
    st.write(f"학습 데이터 샘플 수: {len(df)}건")

except Exception as e:
    st.error(f"엔진 오류 발생: {e}")
