# simulator.py
from modules.stats_engine import StatsEngine
from modules.momentum_engine import MomentumEngine
from modules.weather_engine import WeatherEngine
from modules.bayesian_updater import BayesianUpdater
from modules.odds_engine import OddsEngine

class Simulator:
    @staticmethod
    def get_final_prediction(game_data):
        """
        모든 모듈의 분석 결과를 종합하여 최종 승률 산출
        """
        # 1. 데이터 파싱 및 가중치 적용
        # 각 엔진이 독립적으로 계산한 값을 가져옵니다.
        s_score = StatsEngine.analyze(game_data)
        m_score = MomentumEngine.get_trend(game_data)
        w_score = WeatherEngine.impact_factor(game_data)
        
        # 2. 앙상블 조합 (각 엔진의 영향력 계수 적용)
        # 예: 성능이 입증된 StatsEngine에 가중치를 더 줌
        ensemble_score = (s_score * 0.5) + (m_score * 0.3) + (w_score * 0.2)
        
        # 3. 베이지안 업데이트로 실시간 보정
        # 과거 오차를 반영하여 최종 확률 튜닝
        final_win_prob = BayesianUpdater.update(ensemble_score, game_data['game_id'])
        
        # 4. 배당률 엔진과 비교하여 기대값 확인 (Inefficiency 분석)
        value_bet = OddsEngine.check_value(final_win_prob, game_data['odds'])
        
        return {
            "win_prob": final_win_prob,
            "value_index": value_bet,
            "prediction_ts": "2026-06-30"
        }
