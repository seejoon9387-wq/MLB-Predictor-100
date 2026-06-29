import streamlit as st
import pandas as pd
import ast

# 1. 파일 설정 (깃허브에 올린 파일명과 일치해야 합니다)
FILE_PATHS = {
    "batters": "batters.csv.csv",
    "pitchers": "pitchers.csv.csv",
    "schedule": "schedule.csv.csv",
    "full_data": "mlb_full_data_slim.csv" 
}

# 2. 데이터 로드 및 정제 함수
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        
        # JSON 문자열 컬럼이 있다면 펼치기 (데이터 정제)
        for col in df.columns:
            # 데이터 샘플 확인 (비어있지 않은 첫 번째 값)
            sample = df[col].dropna()
            if not sample.empty and isinstance(sample.iloc[0], str) and sample.iloc[0].startswith('{'):
                expanded = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
                expanded_df = pd.json_normalize(expanded)
                # 컬럼명 충돌 방지를 위해 접두사 추가
                expanded_df.columns = [f"{col}_{subcol}" for subcol in expanded_df.columns]
                df = pd.concat([df.drop(columns=[col]), expanded_df], axis=1)
        return df
    except Exception as e:
        st.error(f"파일 로딩 오류 ({file_path}): {e}")
        return None

# 3. 메인 화면 구성
def main():
    st.set_page_config(page_title="MLB 분석 엔진", layout="wide")
    st.title("⚾ MLB 분석 엔진")
    
    # 데이터 로드
    all_data = {}
    for key, path in FILE_PATHS.items():
        data = load_data(path)
        if data is not None:
            all_data[key] = data
    
    if not all_data:
        st.error("데이터 파일을 찾을 수 없습니다. 깃허브 폴더를 확인하세요.")
        return

    # 사이드바 메뉴
    st.sidebar.title("메뉴")
    menu = st.sidebar.radio("분석 선택", ["데이터 요약", "선수 검색"])
    dataset = st.sidebar.selectbox("데이터셋 선택", list(all_data.keys()))
    
    # 기능 실행
    if menu == "데이터 요약":
        st.subheader(f"📊 {dataset} 데이터 미리보기")
        st.dataframe(all_data[dataset], use_container_width=True)
        
    elif menu == "선수 검색":
        st.subheader("🔍 선수/데이터 검색")
        query = st.text_input("검색어를 입력하세요 (예: 선수 이름, 팀 등)")
        if query:
            df = all_data[dataset]
            # 모든 컬럼에서 검색
            mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
            result = df[mask]
            st.write(f"검색 결과: {len(result)}건")
            st.dataframe(result, use_container_width=True)

if __name__ == "__main__":
    main()
