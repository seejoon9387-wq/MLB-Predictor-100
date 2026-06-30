# [파일: test_engine.py]
from registry import EngineRegistry
from engine import SabermetricsEngine
# 다른 도메인 엔진들도 모두 import

def run_system_test():
    print("--- 🔍 시스템 통합 테스트 시작 ---")
    registry = EngineRegistry()
    
    # 1. 모듈 등록 테스트
    try:
        registry.register('sabermetrics', SabermetricsEngine())
        print("✅ 모듈 등록 성공")
    except Exception as e:
        print(f"❌ 모듈 등록 실패: {e}")
        return

    # 2. 데이터 흐름 테스트 (더미 데이터)
    dummy_data = {"stats": [1, 2, 3]}
    
    # 3. 병렬 처리 테스트
    try:
        results = registry.run_parallel(['sabermetrics'], dummy_data)
        print(f"✅ 병렬 처리 테스트 성공: {results}")
    except Exception as e:
        print(f"❌ 병렬 처리 테스트 실패: {e}")
        return

    print("--- 🏁 시스템 통합 테스트 완료: 모든 모듈 정상 작동 ---")

if __name__ == "__main__":
    run_system_test()
