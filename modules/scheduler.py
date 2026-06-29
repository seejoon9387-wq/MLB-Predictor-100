# modules/scheduler.py
from apscheduler.schedulers.blocking import BlockingScheduler
from main_trainer import MLBUnifiedTrainer

def daily_retraining_job():
    print("일일 자동 재학습 작업 시작...")
    trainer = MLBUnifiedTrainer()
    trainer.run()
    print("재학습 완료 및 모델 업데이트 성공.")

scheduler = BlockingScheduler()
# 매일 새벽 4시(경기가 모두 종료된 후)에 재학습 실행
scheduler.add_job(daily_retraining_job, 'cron', hour=4, minute=0)

if __name__ == "__main__":
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
