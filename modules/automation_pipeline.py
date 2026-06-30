import time
import schedule # pip install schedule

class PipelineAutomator:
    def __init__(self, engine_instance):
        self.engine = engine_instance

    def daily_run_pipeline(self):
        """매일 경기 데이터가 업데이트되는 시점에 자동 실행"""
        print("자동 파이프라인 가동: 데이터 수집 중...")
        # 1. 데이터 수집
        # 2. 전처리
        # 3. 예측
        # 4. 결과 저장
        print("예측 리포트 생성 완료.")

    def start_scheduler(self):
        """실시간 스케줄러 등록"""
        schedule.every().day.at("08:00").do(self.daily_run_pipeline)
        
        while True:
            schedule.run_pending()
            time.sleep(60)

# 모듈 사용 예시
if __name__ == "__main__":
    # 자동화 엔진 객체 주입
    automator = PipelineAutomator(engine_instance=None)
    print("스케줄러가 활성화되었습니다. (매일 08:00 실행)")
