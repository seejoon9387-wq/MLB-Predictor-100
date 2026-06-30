import streamlit as st
import pandas as pd
import requests
import io
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

st.title("MLB 예측 분석 엔진 v1.2 (Stable)")

FILE_ID = "1iSbcXGYzInvd5LQ1jLqdq0MgMtTT09pw"
DATA_URL = f"https://drive.usercontent.com/download?id={FILE_ID}&export=download&confirm=t"

@st.cache_data
def load_data():
    # 데이터를 청크 단위로 읽거나 최소한으로 로드
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(DATA_URL, headers=headers)
    # 필요한 컬럼만 가져오기 + 데이터타입 최적화
    use_cols = ['launch_speed', 'launch_angle', 'bat_speed', 'release_speed', 'hyper_speed']
    df = pd.read_csv(io.BytesIO(response.content), usecols=use_cols)
    return df.dropna()

try:
    with st.spinner('안정적인 엔진 부팅 중...'):
        df = load_data()
        
        # 타겟 설정
        df['hit_binary'] = (df['launch_speed'] > 95).astype(int)
        
        # 학습 데이터 선택
        features = ['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed']
        X = df[features]
        y = df['hit_binary']
        
        # 모델 학습 (가장 가벼운 설정)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        model = RandomForestClassifier(n_estimators=50, max_depth=5, n_jobs=-1, random_state=42)
        model.fit(X_train, y_train)
        
        acc = accuracy_score(y_test, model.predict(X_test))
        st.success(f"### 엔진 가동 성공! 예측 정확도: {acc:.4f}")
        
except Exception as e:
    st.error(f"엔진 부팅 오류: {e}")
    st.write("메모리 부족 문제일 수 있습니다. 'Manage App'에서 로그를 확인하거나 데이터를 더 줄여야 할 수 있습니다.")
