import pandas as pd
import numpy as np

def calculate_sabermetrics(df):
    """
    타자: wRC+ (기초)
    투수: FIP (수비무관 방어율), SIERA (투수 성적 예측 지표)
    """
    # 1. 투수 지표: FIP (상수 C는 리그 평균 방어율로 가정)
    # FIP = ((13*HR + 3*(BB+HBP) - 2*K) / IP) + C
    df['fip'] = ((13 * df.get('hr', 0) + 3 * (df.get('bb', 0) + df.get('hbp', 0)) - 2 * df.get('so', 0)) / df.get('ip', 1)) + 3.20

    # 2. 타자 지표: wRC+ (간소화 버전)
    # wRC = (((woba - league_woba) / woba_scale) + (league_r/pa)) * pa
    # wRC+ = (wRC / league_wRC) * 100
    df['wrc_plus'] = (df.get('woba', 0.320) / 0.320) * 100 
    
    # 3. 투수 지표: SIERA (간소화 모델)
    df['siera'] = 6.145 - 16.986 * (df.get('so', 0) / df.get('pa', 1)) + 11.434 * (df.get('bb', 0) / df.get('pa', 1)) - 1.858 * ((df.get('gb', 0) - df.get('fb', 0)) / df.get('pa', 1))

    return df[['game_pk', 'fip', 'wrc_plus', 'siera']]
