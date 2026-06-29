class Registry:
    _data = {}

    @classmethod
    def register(cls, key, value):
        """각 모듈이 자신의 연산 결과를 이곳에 등록"""
        cls._data[key] = value

    @classmethod
    def get_all_engine_results(cls):
        """모든 엔진의 결과를 통합해서 반환"""
        return cls._data

    @classmethod
    def clear(cls):
        cls._data = {}
