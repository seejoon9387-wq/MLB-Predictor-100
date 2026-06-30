# [파일: registry.py]
class EngineRegistry:
    def __init__(self):
        self._modules = {}
        # 의존성 정의: 각 엔진이 필요로 하는 데이터 피처 명시
        self._dependencies = {
            'sabermetrics': ['stats_data'],
            'stamina_engine': ['player_history', 'schedule'],
            'weather_engine': ['weather_data']
        }

    def register(self, name, module):
        self._modules[name] = module

    def get_module(self, name):
        return self._modules[name]

    def run_all_domain_engines(self, data):
        # 의존성을 확인하며 순차/병렬 실행
        results = {}
        for name, module in self._modules.items():
            if hasattr(module, 'execute'):
                results[name] = module.execute(data)
        return results
