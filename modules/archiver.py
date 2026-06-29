import pandas as pd
import os
import shutil

def archive_old_data(df, archive_path="archives"):
    """
    데이터 아카이빙:
    - 특정 시점(예: 이전 연도)의 데이터를 메인 데이터셋에서 분리
    - 'archives/' 폴더로 이동하여 보관
    """
    if not os.path.exists(archive_path):
        os.makedirs(archive_path)
    
    # 예시: 2025년 이전 데이터는 아카이브 대상으로 간주
    archive_mask = df['game_year'] < 2025
    archive_df = df[archive_mask]
    
    if not archive_df.empty:
        # 아카이브 파일 저장 (CSV)
        archive_file = os.path.join(archive_path, "mlb_data_archive.csv")
        archive_df.to_csv(archive_file, index=True)
        
        # 메인 데이터셋에서 아카이브된 데이터 제거
        df = df[~archive_mask]
        
    return df
