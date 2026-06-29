import streamlit as st

def show(data):
    st.subheader("선수 검색 모듈")
    dataset_name = st.selectbox("데이터셋 선택", list(data.keys()))
    df = data[dataset_name]
    
    search_query = st.text_input("검색어 입력")
    
    if search_query:
        # 모든 컬럼에 대해 검색어가 포함된 행을 찾음
        mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        st.write("데이터셋을 검색하세요.")
