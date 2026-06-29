import pandas as pd

def set_time_index(df, date_col='date'):
    """
    데이터프레임에서 날짜 컬럼을 찾아 datetime 타입으로 변환하고 인덱스로 설정합니다.
    """
    if date_col in df.columns:
        # 1. 날짜형으로 변환 (오류 발생 시 무시하도록 설정)
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        # 2. 인덱스 설정
        df = df.set_index(date_col)
        # 3. 시간 순서대로 정렬
        df = df.sort_index()
    return df
