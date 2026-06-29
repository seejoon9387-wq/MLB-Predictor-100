import streamlit as st
import pandas as pd
import os

# 버전 정보
ENGINE_VERSION = "1.0.0"

# 데이터 파일 경로 (구글 드라이브/로컬 환경에 맞춰 수정 가능)
DATA_FILES = {
    "batters": "batters_master_clean.csv",
    "pitchers": "pitchers_master_clean.csv",
    "full_data": "mlb_full_data.csv",
    "schedule": "mlb_2024_2026_schedule.csv"
}

@st.cache_data
def load_all_data():
    """엔진 데이터 로딩 및 무결성 검증 함수"""
    data = {}
    errors = []
    
    for key, filename in DATA_FILES.items():
        try:
            # 1. 파일 존재 여부 확인
            if not os.path.exists(filename):
                errors.append(f"파일 누락: {filename}")
                continue
                
            # 2. 파일 로딩 (메모리 최적화)
            df = pd.read_csv(filename)
            data[key] = df
            
        except Exception as e:
            errors.append(f"로딩 실패 ({filename}): {str(e)}")
            
    return data, errors

def main():
    st.title(f"MLB 분석 엔진 v{ENGINE_VERSION}")
    
    # 데이터 로드
    data, errors = load_all_data()
    
    # 3. 에러 발생 시 알림
    if errors:
        for err in errors:
            st.error(err)
        st.stop() # 데이터가 없으면 진행 불가
        
    st.success("모든 데이터가 성공적으로 엔진에 연동되었습니다.")
    
    # 데이터 연동 구조 확인을 위한 관계형 모델 시각화 전략
    st.subheader("데이터 연동 구조")
    st.info("각 데이터는 'player_id'와 'game_pk'를 기준으로 통합됩니다.")
    
    # 간략한 데이터 요약 출력
    if st.checkbox("데이터프레임 정보 확인"):
        for name, df in data.items():
            st.write(f"### {name}")
            st.write(f"행: {df.shape[0]}, 열: {df.shape[1]}")

if __name__ == "__main__":
    main()
