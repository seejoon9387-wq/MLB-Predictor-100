import streamlit as st
import pandas as pd
import requests
import io
from sklearn.ensemble import RandomForestClassifier

st.title("MLB 최후의 엔진 가동 (테스트용)")

# 가장 첫 번째 파트만 로드
FILE_ID = "1Vv1bVp9e1IgP8dU5OQRSkJUFIDpqsye5"
URL = f"https://drive.usercontent.google.com/download?id={FILE_ID}&export=download&confirm=t"

if st.button("테스트 학습 시작"):
    with st.spinner('파트 1 데이터 로드 중...'):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(URL, headers=headers)
            df = pd.read_csv(io.BytesIO(response.content), nrows=20000) # 2만행만 학습
            df = df.dropna()
            
            X = df[['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed']]
            y = (df['launch_speed'] > 95).astype(int)
            
            model = RandomForestClassifier(n_estimators=10, max_depth=3)
            model.fit(X, y)
            
            st.success("학습 완료!")
            st.write(f"테스트 정확도: {model.score(X, y):.4f}")
            
        except Exception as e:
            st.error(f"오류: {e}")
            st.write("만약 여기서도 에러가 난다면 구글 드라이브 권한 문제일 가능성이 큽니다.")
