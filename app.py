import streamlit as st
import pandas as pd
import requests
import io
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

st.title("MLB 예측 분석 엔진 v1.3 (Memory-Safe)")

FILE_ID = "1iSbcXGYzInvd5LQ1jLqdq0MgMtTT09pw"
DATA_URL = f"https://drive.usercontent.google.com/download?id={FILE_ID}&export=download&confirm=t"

@st.cache_data
def load_data_safe():
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(DATA_URL, headers=headers)
    
    # 1.4GB 전체가 아닌, 앞의 100,000행만 읽어서 메모리 오버로드 방지
    use_cols = ['launch_speed', 'launch_angle', 'bat_speed', 'release_speed', 'hyper_speed']
    df = pd.read_csv(io.BytesIO(response.content), usecols=use_cols, nrows=100000)
    return df.dropna()

try:
    with st.spinner('메모리 안정화 로딩 중...'):
        df = load_data_safe()
        
        # 타겟 설정
        df['hit_binary'] = (df['launch_speed'] > 95).astype(int)
        
        # 피처 및 학습
        features = ['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed']
        X = df[features]
        y = df['hit_binary']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 모델 복잡도 축소 (학습 속도 및 안정성 극대화)
        model = RandomForestClassifier(n_estimators=30, max_depth=5, n_jobs=-1)
        model.fit(X_train, y_train)
        
        acc = accuracy_score(y_test, model.predict(X_test))
        st.success(f"### 엔진 가동 성공! (부분 학습 데이터 기준)")
        st.write(f"예측 정확도: {acc:.4f}")
        st.write(f"사용된 데이터 샘플: {len(df)}건")

except Exception as e:
    st.error(f"엔진 오류 발생: {e}")
    st.write("메모리 용량 내에서 데이터를 불러오는 데 실패했습니다.")
