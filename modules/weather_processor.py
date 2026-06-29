import pandas as pd

def process_weather_features(df):
    """
    기상 데이터를 모델링 가능한 형태로 변환 및 정규화
    """
    # 1. 필수 기상 컬럼이 있는지 확인 (데이터셋에 따라 이름 확인 필요)
    weather_cols = ['temp', 'wind_speed', 'humidity']
    for col in weather_cols:
        if col not in df.columns:
            # 데이터가 없을 경우 평균값으로 채우거나 0 처리
            df[col] = 70.0 if col == 'temp' else 0.0
    
    # 2. 상대적 기상 지표 생성 (리그 평균과의 차이)
    # 기온은 타구 비거리에 비례하므로 리그 평균(예: 75도)과의 차이로 변환
    df['temp_deviation'] = df['temp'] - 75.0
    
    # 3. 바람 보정 (바람의 방향과 세기를 결합하는 것이 이상적이나, 
    # 여기서는 단순 풍속을 에너지 성분으로 변환)
    df['wind_energy'] = df['wind_speed'] ** 2
    
    # 4. 습도 보정 (밀도 지수)
    # 습도가 높으면 공기 밀도가 낮아짐 (일반적인 물리학 법칙 적용)
    df['air_density_idx'] = 1 - (df['humidity'] / 100) * 0.1
    
    return df
