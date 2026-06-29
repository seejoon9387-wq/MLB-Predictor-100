import streamlit as st

def show_column_names(df):
    st.subheader("🔍 데이터 컬럼 리스트 (전체)")
    
    # 리스트를 가로로 길게 출력하여 한눈에 보게 함
    cols = df.columns.tolist()
    st.write(cols)
    
    st.info("💡 위 리스트를 복사해서 저에게 알려주세요! 그 안에 날짜 정보가 어디 있는지 제가 찾아드릴게요.")
