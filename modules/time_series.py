import pandas as pd

def set_time_index(df):
    """
    game_pk를 사용하여 데이터를 시간 순서대로 정렬하고 인덱스로 설정합니다.
    """
    if 'game_pk' in df.columns:
        df = df.set_index('game_pk')
        df = df.sort_index()
    return df
