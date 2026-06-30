import streamlit as st
import pandas as pd
import requests
import io
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

st.title("MLB 예측 분석 엔진 v1.4 (Safe-Load)")

# 파일 ID
FILE_ID = "1iSbcXGYzInvd5LQ1jLqdq0MgMtTT09pw"
DATA_URL = f"https://drive.usercontent.google.com/download?id={FILE_ID}&export=download&confirm=t"

st.write("서버 메모리 보호를 위해 '엔진 가동' 버튼을 눌러야 데이터를 로드합니다.")

if st.button("엔진 가동 (데이터 로드 시작)"):
    try:
        with st.spinner('데이터를 처리하는 중... (메모리 사용 최적화)'):
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(DATA_URL, headers=headers)
            
            # 데이터를 더 작게 읽음 (샘플링)
            use_cols = ['launch_speed', 'launch_angle', 'bat_speed', 'release_speed', 'hyper_speed']
            df = pd.read_csv(io.BytesIO(response.content), usecols=use_cols, nrows=50000)
            df = df.dropna()
            
            df['hit_binary'] = (df['launch_speed'] > 95).astype(int)
            
            features = ['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed']
            X = df[features]
            y = df['hit_binary']
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=20, max_depth=3, n_jobs=-1)
            model.fit(X_train, y_train)
            
            acc = accuracy_score(y_test, model.predict(X_test))
            st.success(f"### 분석 완료! 예측 정확도: {acc:.4f}")
            
    except Exception as e:
        st.error(f"서버 메모리 한계로 로드 실패: {e}")
        st.write("데이터가 너무 커서 서버에서 처리할 수 없습니다. 데이터를 100MB 이하로 줄여서 업로드해야 합니다.")
