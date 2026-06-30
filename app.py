import streamlit as st
import pandas as pd
import requests
import io
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

st.title("MLB 예측 분석 엔진 v1.1 (High-Precision)")

FILE_ID = "1iSbcXGYzInvd5LQ1jLqdq0MgMtTT09pw"
DATA_URL = f"https://drive.usercontent.google.com/download?id={FILE_ID}&export=download&confirm=t"

@st.cache_data
def load_data(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    # 필요한 컬럼만 선택하여 로드
    use_cols = ['launch_speed', 'launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension']
    df = pd.read_csv(io.BytesIO(response.content), usecols=use_cols)
    return df.dropna()

try:
    with st.spinner('엔진 데이터 캘리브레이션 중...'):
        df = load_data(DATA_URL)
        df['hit_binary'] = (df['launch_speed'] > 95).astype(int)
        
        features = ['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension']
        X = df[features]
        y = df['hit_binary']
        
        # 과적합 방지를 위해 학습/테스트 데이터 분리
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # 모델의 복잡도를 제어 (max_depth 10 -> 8, min_samples_leaf 추가)
        model = RandomForestClassifier(n_estimators=100, max_depth=8, min_samples_leaf=5, n_jobs=-1, random_state=42)
        model.fit(X_train, y_train)
        
        # 결과 보고
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        st.success(f"### 엔진 예측 정확도 (검증 데이터 기준): {acc:.4f}")
        st.write("---")
        st.write("### 예측 품질 보고서")
        st.text(classification_report(y_test, y_pred))
        
except Exception as e:
    st.error(f"엔진 오류: {e}")
