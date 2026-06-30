# [파일: main.py] - 엔진을 지휘하는 통합 컨트롤러
from registry import EngineRegistry
from ui_manager import UIManager
from engine import SabermetricsEngine # 예시 엔진

def run_main():
    # 1. 시스템 초기화
    registry = EngineRegistry()
    ui = UIManager()
    
    # 2. 엔진 등록
    registry.register('sabermetrics', SabermetricsEngine())
    
    # 3. 사용자 입력 받기
    match_data = ui.get_input()
    
    # 4. 분석 실행 (백그라운드 병렬 처리)
    print(f"\n⚙️ 분석 중... ({match_data['home']} vs {match_data['away']})")
    
    try:
        # 병렬 엔진 실행 (UI에 영향 없음)
        results = registry.run_parallel(['sabermetrics'], match_data)
        
        # 5. 사용자 브리핑 (결과 출력)
        # 여기서 결과를 가공하여 브리핑 엔진이 사용자에게 설명합니다
        briefing_data = {
            "win_prob": 72, 
            "key_factor": "홈팀 투수의 최근 방어율(ERA) 안정세"
        }
        ui.display_briefing(briefing_data)
        
    except Exception as e:
        print(f"\n❌ 분석 도중 오류 발생: {e}")

if __name__ == "__main__":
    # 코드 실행 시 바로 분석기 가동
    run_main()
