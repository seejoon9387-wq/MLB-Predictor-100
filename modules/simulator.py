import pandas as pd
import numpy as np
import os

class Simulator:
    @staticmethod
    def load_data():
        # 데이터 파일이 있는 경로를 확인하고 읽습니다.
        # 파일명이 다르면 아래 'mlb_games.csv' 부분을 실제 파일명으로 바꾸세요.
        if os.path.exists('mlb_games.csv'):
            return pd.read_csv('mlb_games.csv')
        return pd.DataFrame()

    @staticmethod
    def calculate_win_probability(home_team, away_team):
        df = Simulator.load_data()
        if df.empty:
            return 50.0
        
        # 팀별 데이터 필터링
        home_data = df[df['team'] == home_team]
        away_data = df[df['team'] == away_team]
        
        if home_data.empty or away_data.empty:
            return 50.0

        # 승리 기여 지수 계산 (공식: OPS + wOBA - ERA 기반)
        # 데이터에 있는 컬럼들을 활용하여 간단한 승률 계산식을 만듭니다.
        home_score = (home_data['ops'].mean() * 0.5) + (1 / (home_data['era'].mean() + 0.1) * 0.5)
        away_score = (away_data['ops'].mean() * 0.5) + (1 / (away_data['era'].mean() + 0.1) * 0.5)
        
        # 로지스틱 함수를 사용해 0~100 사이의 승률로 변환
        prob = 1 / (1 + np.exp(-(home_score - away_score)))
        return round(prob * 100, 2)

# 사용 예시: (app.py 등에서 아래처럼 호출하시면 됩니다)
# from simulator import Simulator
# result = Simulator.calculate_win_probability("LAD", "NYY")
# print(f"홈팀 승리 예상 확률: {result}%")
