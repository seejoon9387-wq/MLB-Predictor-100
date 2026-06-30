class SabermetricsEngine:
    def __init__(self):
        pass

    def execute(self, data):
        # 함수 내부에서 import하여 순환 참조 방지
        from modules.config import SCHEMA
        
        # 분석 로직 (예시)
        prob = 65.0
        return {'win_prob': prob, 'schema_applied': list(SCHEMA.keys())}
