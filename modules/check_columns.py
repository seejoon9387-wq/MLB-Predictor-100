import streamlit as st

def show_column_names(df):
    st.subheader("🔍 데이터 컬럼 확인 (디버깅 모드)")
    
    # 리스트를 그냥 출력하지 말고, 어떤 컬럼이 있는지 전체를 보여줍니다.
    cols = df.columns.tolist()
    st.write("전체 컬럼 리스트:", cols)
    
    # 대소문자 구분 없이 'date'를 포함하는지 다시 정밀 검사
    found = False
    for col in cols:
        if 'date' in col.lower():
            st.success(f"발견! 날짜 관련 컬럼명: {col}")
            found = True
    
    if not found:
        st.error("주의: 컬럼 목록에 'date'라는 단어가 포함된 것이 하나도 없습니다. 데이터를 다시 확인해야 합니다.")
