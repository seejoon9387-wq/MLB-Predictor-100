import streamlit as st
import pandas as pd

# 버전 정보
ENGINE_VERSION = "1.0.0"

# 구글 드라이브 공유 링크 (데이터 로딩용)
DATA_URLS = {
    "batters": "https://docs.google.com/spreadsheets/d/1UAgU7QH65LOqAaicg-Snrn26wfniDOWT/export?format=csv",
    "pitchers": "https://docs.google.com/spreadsheets/d/1jNHpBgB_NXuI5Aedw5j0qG05u9eSFyHT/export?format=csv",
    "full_data": "https://docs.google.com/spreadsheets/d/1vj_n2MOPjAQ50U4N5KAxKxwuoL3UCaI4/export?format=csv",
    "schedule": "https://docs.google.com/spreadsheets/d/1jNvhwD_1nQhW9pnyVodutjtZfY03b4-Q/export?format=csv"
}

@st.cache_data
def load_all_data():
    """구글 드라이브에서 데이터를 읽어오는 엔진 함수"""
    data = {}
    errors = []
    
    for key, url in DATA_URLS.items():
        try:
            # 웹 URL을 통해 CSV 데이터를 읽음
            df = pd.read_csv(url)
            data[key] = df
        except Exception as e:
            errors.append(f"로딩 실패 ({key}): {str(e)}")
            
    return data, errors

def main():
    st.set_page_config(page_title="MLB 분석 엔진", layout="wide")
    st.title(f"⚾ MLB 분석 엔진 v{ENGINE_VERSION}")
    
    # 1. 데이터 로드 실행
    with st.spinner('데이터를 엔진에 연동 중입니다...'):
        data, errors = load_all_data()
    
    # 2. 에러 체크
    if errors:
        for err in errors:
            st.error(err)
        st.warning("데이터를 불러올 수 없습니다. 구글 드라이브 공유 설정을 '링크가 있는 모든 사용자'로 변경했는지 확인하세요.")
        st.stop()
        
    st.success("데이터 연동 완료!")
    
    # 3. 데이터 확인 테이블
    st.subheader("연동된 데이터 요약")
    summary_data = []
    for name, df in data.items():
        summary_data.append({"데이터셋": name, "행 개수": len(df), "열 개수": len(df.columns)})
    
    st.table(pd.DataFrame(summary_data))

    # 4. 분석 시작 안내
    st.info("이제 이 데이터를 활용해 차트를 그리거나 통계를 낼 준비가 되었습니다.")

if __name__ == "__main__":
    main()
