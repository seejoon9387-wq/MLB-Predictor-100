import pandas as pd
from modules.simulator import simulate_match_scenarios

class MLBUnifiedTrainer:
    def __init__(self, data=None):
        """
        초기화 시 데이터를 선택적으로 받으며,
        데이터가 없어도 에러를 발생시키지 않도록 설계함.
        """
        self.data = data if data is not None else pd.DataFrame()

    def analyze(self, input_data):
        """
        데이터를 분석하여 최종 리포트를 반환합니다.
        input_data가 딕셔너리든 데이터프레임이든 모두 안전하게 처리합니다.
        """
        try:
            # 1. 데이터를 항상 시리즈/딕셔너리처럼 다룰 수 있게 표준화
            # KeyError 방지를 위해 .get() 사용이 필수
            if isinstance(input_data, dict):
                game_pk = input_data.get('game_pk', 'Unknown')
                data_for_sim = input_data
            else:
                # 데이터프레임의 첫 번째 행을 딕셔너리로 변환
                data_for_sim = input_data.to_dict() if hasattr(input_data, 'to_dict') else input_data
                game_pk = data_for_sim.get('game_pk', 'Unknown')

            # 2. 시뮬레이터 실행
            sim_result = simulate_match_scenarios(data_for_sim)

            # 3. 분석 결과 리포트 생성 (방어적 구조)
            report = {
                'winner': 'Home' if sim_result > 0.5 else 'Away',
                'confidence': round(min(abs(sim_result - 0.5) * 200, 99.9), 1),
                'detailed_report': f"게임 ID {game_pk}에 대한 분석이 완료되었습니다. "
                                   f"산출된 로직 점수는 {sim_result:.2f}입니다."
            }
            return report

        except Exception as e:
            # 엔진 내부에서 문제가 생겨도 앱을 죽이지 않고 에러 메시지만 반환
            return {
                'error': str(e),
                'status': 'failed',
                'message': '분석 엔진에서 처리할 수 없는 데이터 구조입니다.'
            }
