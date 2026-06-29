import streamlit as st

def show(data):
    st.subheader("데이터 요약 모듈")
    for name, df in data.items():
        st.write(f"### [데이터셋: {name}]")
        # 데이터프레임으로 변환된 상태라면 정상 출력됩니다.
        st.dataframe(df.head(10), use_container_width=True)
