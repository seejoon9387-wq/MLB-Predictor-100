from registry import EngineRegistry
from ui_manager import UIManager
from engine import SabermetricsEngine
from briefing_engine import get_briefing # 가정: 결과 해석을 담당하는 모듈

def run_main():
    # 1. 시스템 초기화
    registry = EngineRegistry()
    ui = UIManager()
    
    # 2. 엔진 등록 (우리가 만든 통합 엔진)
    registry.register('sabermetrics', SabermetricsEngine())
    
    # 3. 사용자 입력 받기
    match_data = ui.get_input()
    
    # 4. 분석 실행
    print(f"\n⚙️ 분석 중... ({match_data['home']} vs {match_data['away']})")
    
    try:
        # 엔진 실행 (결과값은 registry를 통해 딕셔너리로 반환됨)
        # run_parallel 결과는 {엔진이름: 결과값} 형태일 것임
        results = registry.run_parallel(['sabermetrics'], match_data)
        engine_result = results.get('sabermetrics', {})
        
        # 5. 브리핑 엔진 호출 (결과 데이터 전달)
        # 이제 고정 데이터가 아니라 실제 계산된 결과를 브리핑함
        briefing_data = get_briefing(engine_result)
        ui.display_briefing(briefing_data)
        
    except Exception as e:
        print(f"\n❌ 분석 도중 오류 발생: {e}")
        # 오류 상세 로그 기록 (logger.py 활용 가능)

if __name__ == "__main__":
    run_main()
