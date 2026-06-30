import streamlit as st
import pandas as pd
import requests
import io
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

st.title("MLB 배치 학습 예측 엔진 v2.0")

# 10개 파일의 ID 리스트
FILE_IDS = [
    "1Vv1bVp9e1IgP8dU5OQRSkJUFIDpqsye5", "10yw1Pv0G93J7RXDBrAsDtBHi2UHMePqz",
    "1XJ-saQyitPfNWm1HqUccKxCRn52p1gJB", "1Pq5-sRx7F44VG5LIpavx6qtFSO2i5klx",
    "1smBQ_lSW5mmE_7Zr8dagajllx9E2ZG1N", "1A4oU4dVMZ1O0_ZBawy1Qf8DJTzs9se9-",
    "1Lv3eJ8hluf3s6HBBA0raXUDvTwkIQZ6-", "1CW-HHudXA2gKgjsKm0izDKXBnuhVVzUQ",
    "1MRjcQuAchgsO0r5NJqOEhHLYQYSPVXFf", "1mjoZ5sQSMBlkjk9Fh9Ywng8zB1pjbWGw"
]

# 모델 초기화 (warm_start=True는 누적 학습을 가능하게 합니다)
model = RandomForestClassifier(n_estimators=10, max_depth=5, n_jobs=-1, warm_start=True)

if st.button("배치 학습 시작 (10개 파트 연동)"):
    try:
        all_accuracies = []
        progress_bar = st.progress(0)
        
        for i, fid in enumerate(FILE_IDS):
            st.write(f"파트 {i+1} 처리 중...")
            url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
            
            # 데이터 로드
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            df = pd.read_csv(io.BytesIO(response.content))
            df = df.dropna()
            
            # 타겟 및 피처 설정
            df['hit_binary'] = (df['launch_speed'] > 95).astype(int)
            features = ['launch_angle', 'bat_speed', 'release_speed', 'hyper_speed', 'release_extension']
            X = df[features]
            y = df['hit_binary']
            
            # 모델 업데이트 (n_estimators를 점점 늘리며 학습)
            model.n_estimators += 10
            model.fit(X, y)
            
            # 파트별 정확도 기록
            acc = accuracy_score(y, model.predict(X))
            all_accuracies.append(acc)
            progress_bar.progress((i + 1) / 10)
            
        st.success("### 모든 데이터 학습 완료!")
        st.write(f"최종 평균 정확도: {sum(all_accuracies)/len(all_accuracies):.4f}")
        
    except Exception as e:
        st.error(f"엔진 오류 발생: {e}")
        st.write("터미널 로그를 확인하여 연결 상태를 재점검하세요.")
