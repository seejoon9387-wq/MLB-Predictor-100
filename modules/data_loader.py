import streamlit as st
import pandas as pd
import zipfile
import os
from modules.registry import create_main_registry
# ... (다른 import 유지)

FILE_NAME = "mlb_full_data_slim.zip"

@st.cache_data
def load_data(analysis_mode="연속적"):
    if not os.path.exists(FILE_NAME):
        return pd.DataFrame()
    
    with zipfile.ZipFile(FILE_NAME, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)
    
    # 1. 컬럼 소문자화 (필수)
    df.columns = [c.lower().strip() for c in df.columns]
    
    # [디버깅] 데이터 확인
    st.write(f"총 로드된 데이터 행 수: {len(df)}")
    st.write("컬럼 목록:", df.columns.tolist())
    
    if 'game_pk' not in df.columns:
        st.error("데이터에 'game_pk'가 없습니다!")
        return pd.DataFrame()
    
    # 2. 파이프라인 (기존 로직)
    # ... (생략: 기존 정제 함수들 호출)
    
    # 3. 레지스트리 생성 전 샘플 확인
    registry = create_main_registry(df)
    
    st.write(f"레지스트리 생성 후 데이터 수: {len(registry)}")
    return registry
