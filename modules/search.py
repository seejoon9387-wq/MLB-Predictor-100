import streamlit as st

def show(data):
    st.subheader("선수 검색 모듈")
    
    # 데이터셋 선택
    dataset_name = st.selectbox("데이터셋 선택", list(data.keys()))
    df = data[dataset_name]
    
    # 검색어 입력
    search_query = st.text_input("선수 이름(또는 ID) 검색")
    
    if search_query:
        # 데이터프레임에서 이름이 포함된 행 필터링 (컬럼명은 데이터에 맞게 수정 필요)
        # 예: 'name' 컬럼이 있다고 가정
        if 'name' in df.columns:
            result = df[df['name'].str.contains(search_query, case=False, na=False)]
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("이 데이터셋에는 'name' 컬럼이 없습니다.")
    else:
        st.write("검색어를 입력하면 결과가 표로 나타납니다.")
