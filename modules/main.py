# [파일: main.py] - 시스템의 통합 관리자 및 실행 파일
import multiprocessing as mp
from registry import EngineRegistry
from engine import SabermetricsEngine
from logger import SystemLogger

def run_full_pipeline(game_id):
    """
    전체 분석 파이프라인을 실행하는 메인 제어 함수
    """
    logger = SystemLogger(game_id)
    registry = EngineRegistry()
    
    # 1. 모듈 등록 (필요한 엔진들을 모두 이곳에 등록)
    registry.register('sabermetrics', SabermetricsEngine())
    # registry.register('weather', WeatherEngine()) ... 추가 등록 가능
    
    print(f"--- [START] 게임 ID: {game_id} 분석 시작 ---")
    
    try:
        # 2. 데이터 로드 및 정제 (가상의 data_loader 예시)
        # 실제로는 여기서 각 모듈의 기능을 호출합니다.
        print("데이터 로드 및 정제 중...")
        raw_data = {"stats": [1, 2, 3]} # 테스트용 데이터
        
        # 3. 병렬 도메인 엔진 가동
        print("도메인 엔진 병렬 분석 중...")
        domain_results = registry.run_parallel(['sabermetrics'], raw_data)
        
        # 4. 베이지안 업데이트 및 확률 예측
        # updater = registry.get_module('bayesian_updater')
        # final_prediction = updater.process(domain_results)
        final_prediction = domain_results # 테스트용 대체
        
        # 5. 브리핑 및 아카이브
        # briefing = registry.get_module('briefing_engine').generate(final_prediction)
        # registry.get_module('archiver').save(game_id, briefing)
        
        print(f"--- [SUCCESS] 분석 결과: {final_prediction} ---")
        return final_prediction

    except Exception as e:
        logger.log_error(f"파이프라인 오류: {e}")
        print(f"--- [ERROR] 분석 실패: {e} ---")
        return None

if __name__ == "__main__":
    # Windows에서 병렬 처리를 위한 필수 설정
    run_full_pipeline(game_id="2026-06-30-BASEBALL")
