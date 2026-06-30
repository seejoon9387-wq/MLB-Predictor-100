# [파일: main.py] - 시스템의 통합 관리자
from registry import EngineRegistry
from logger import SystemLogger

def run_analysis_pipeline(game_id):
    # 1. 시스템 초기화 및 로깅 시작
    logger = SystemLogger(game_id)
    registry = EngineRegistry()
    
    try:
        # 2. 데이터 흐름 제어 (Pipeline Flow)
        raw_data = registry.get_module('data_loader').load(game_id)
        clean_data = registry.get_module('processor').execute(raw_data)
        
        # 3. 인텔리전스 레이어 (도메인 엔진들 통합 분석)
        engine_results = registry.run_all_domain_engines(clean_data)
        
        # 4. 확률 업데이트 및 최종 최적화
        prediction = registry.get_module('bayesian_updater').process(engine_results)
        
        # 5. 브리핑 및 아카이브
        brief = registry.get_module('briefing_engine').generate(prediction)
        registry.get_module('archiver').save(game_id, brief)
        
        return brief
        
    except Exception as e:
        logger.log_error(e)
        raise
