# [파일: engine.py]
class BaseEngine:
    def execute(self, data):
        raise NotImplementedError("각 엔진은 execute 메서드를 구현해야 합니다.")

# 예시 도메인 엔진
class SabermetricsEngine(BaseEngine):
    def execute(self, data):
        return {"sabermetrics_score": 0.85} # 분석 로직
