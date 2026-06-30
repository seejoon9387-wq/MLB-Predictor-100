# [파일: main.py]
from registry import EngineRegistry
from engine import SabermetricsEngine
# (기타 필요한 모듈 import...)
from logger import SystemLogger

def run_full_pipeline(game_id):
    logger = SystemLogger(game_id)
    registry = EngineRegistry()
    
    # 1. 모듈 등록
    registry.register('sabermetrics', SabermetricsEngine())
    # registry.register('weather', WeatherEngine()) 등 추가...
    
    try:
        # 2. 데이터 로드 및 정제
        data_loader = registry.get_module('data_loader')
        raw_data = data_loader.load(game_id)
        
        # 3. 병렬 도메인 엔진 가동
        domain_results = registry.run_parallel(['sabermetrics'], raw_data)
        
        # 4. 베이지안 업데이트 및 확률 예측
        updater = registry.get_module('bayesian_updater')
        final_prediction = updater.process(domain_results)
        
        # 5. 브리핑 및 아카이브
        briefing = registry.get_module('briefing_engine').generate(final_prediction)
        registry.get_module('archiver').save(game_id, briefing)
        
        print("분석 완료. 결과 확인:", briefing)
        return briefing

    except Exception as e:
        logger.log_error(f"파이프라인 오류: {e}")
        return None

if __name__ == "__main__":
    run_full_pipeline(game_id="2026-06-30-BASEBALL")

# [파일: main.py] - 맨 아래에 이 내용을 추가하세요
def run_system_test():
    print("\n--- 🔍 시스템 통합 테스트 시작 ---")
    from registry import EngineRegistry
    from engine import SabermetricsEngine
    
    try:
        registry = EngineRegistry()
        registry.register('sabermetrics', SabermetricsEngine())
        print("✅ 모듈 등록 성공")
        
        # 더미 데이터로 병렬 처리 테스트
        results = registry.run_parallel(['sabermetrics'], {"data": [1]})
        print(f"✅ 병렬 처리 테스트 성공: {results}")
        print("--- 🏁 시스템 테스트 완료 --- \n")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")

if __name__ == "__main__":
    # 먼저 시스템 테스트를 수행하고
    run_system_test()
    
    # 그 다음 실제 분석 파이프라인을 실행합니다
    # run_full_pipeline(game_id="2026-06-30-BASEBALL")
