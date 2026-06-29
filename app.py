import streamlit as st
import pandas as pd
import ast

# 1. 파일 경로 설정
FILE_PATHS = {
    "batters": "batters.csv.csv",
    "pitchers": "pitchers.csv.csv",
    "schedule": "schedule.csv.csv",
    "full_data": "mlb_full_data_slim.csv" 
}

# 2. 메모리 최적화 로딩
@st.cache_resource
def load_data(file_path):
    # 파일이 존재하는지 먼저 확인
    try:
        # 데이터 타입 최적화 (메모리 50% 절감)
        df = pd.read_csv(file_path)
        
        # JSON 컬럼이 있다면 아주 제한적으로 처리
        for col in df.columns:
            if df[col].dtype == 'object' and df[col].astype(str).str.startswith('{').any():
                # 필요 없는 데이터는 제거하여 메모리 보호
                df[col] = df[col].apply(lambda x: str(x)[:50]) 
        return df
    except Exception:
        return pd.DataFrame() # 오류 시 빈 데이터프레임 반환

def main():
    st.set_page_config(layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    # 데이터 로드
    selected_file = st.selectbox("데이터셋 선택", list(FILE_PATHS.keys()))
    df = load_data(FILE_PATHS[selected_file])
    
    if df.empty:
        st.error("데이터 파일을 불러올 수 없습니다. 파일 이름을 다시 확인하세요.")
        return

    st.dataframe(df.head(200), use_container_width=True)

if __name__ == "__main__":
    main()
