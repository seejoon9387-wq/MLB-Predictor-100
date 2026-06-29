import streamlit as st

def show_column_names(df):
    """
    데이터프레임의 모든 컬럼명을 출력하여 사용자가 확인할 수 있게 합니다.
    """
    st.subheader("🔍 데이터 컬럼 확인")
    st.write("데이터셋에 포함된 컬럼 목록입니다:")
    
    # 컬럼명을 리스트 형태로 출력
    cols = df.columns.tolist()
    st.write(cols)
    
    # 만약 'date'라는 단어가 포함된 컬럼이 있는지 검색
    date_cols = [c for c in cols if 'date' in c.lower()]
    if date_cols:
        st.success(f"날짜와 관련된 컬럼을 찾았습니다: {date_cols}")
    else:
        st.warning("날짜와 관련된 컬럼을 찾지 못했습니다. 목록을 확인해 주세요.")
