import pandas as pd
from modules.stats_engine import StatsEngine
from modules.momentum_engine import MomentumEngine
from modules.weather_engine import WeatherEngine
from modules.bayesian_updater import BayesianUpdater

class Simulator:
    @staticmethod
    def run_prediction(game_data):
        """
        다양한 모듈의 출력을 앙상블하여 최종 예측 수행
        """
        # 1. 선수/팀 능력치 기반 분석
        stats_score = StatsEngine.get_baseline_score(game_data)
        
        # 2. 최근 기세 및 모멘텀 분석
        momentum_score = MomentumEngine.calculate_trend(game_data)
        
        # 3. 환경 변수 보정
        weather_factor = WeatherEngine.calculate_impact(game_data)
        
        # 4. 베이지안 업데이트 (누적 데이터 기반 보정)
        # 이전 경기들의 오차를 학습하여 현재 예측치 보정
        final_win_prob = BayesianUpdater.update_prob(
            [stats_score, momentum_score, weather_factor], 
            game_data['id']
        )
        
        return final_win_prob

    @staticmethod
    def run_all(schedule_list):
        return [Simulator.run_prediction(g) for g in schedule_list]
