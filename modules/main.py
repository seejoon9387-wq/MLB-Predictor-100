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
