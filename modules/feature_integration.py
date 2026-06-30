import pandas as pd

class FeatureIntegrator:
    def __init__(self, profiler):
        # 3단계에서 만든 PlayerProfiler 인스턴스를 주입받아 사용
        self.profiler = profiler

    def create_feature_snapshot(self, df_player, feature='ops'):
        """
        선수의 최근 성적, 환경 변수, 그리고 통합된 시계열 기울기를 하나의 행으로 병합
        """
        # 3단계에서 구현한 컨디션 지수 및 상세 기울기 호출
        trend_result = self.profiler.calculate_integrated_condition_index(df_player, feature)
        
        # 마지막 경기 데이터 기준으로 통합
        last_row = df_player.iloc[-1].copy()
        
        # 추세 지표 통합
        last_row['condition_index'] = trend_result['index']
        last_row['slope_1d'] = trend_result['details'][1]
        last_row['slope_3d'] = trend_result['details'][3]
        last_row['slope_7d'] = trend_result['details'][7]
        
        return last_row

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    from profiling import PlayerProfiler
    
    # 3단계 profiler 인스턴스 사용
    profiler = PlayerProfiler()
    integrator = FeatureIntegrator(profiler)
    
    # 테스트용 데이터
    df_player = pd.DataFrame({'ops': [0.700, 0.720, 0.750, 0.780, 0.800]})
    
    snapshot = integrator.create_feature_snapshot(df_player)
    
    print("통합된 선수 피처 스냅샷:")
    print(snapshot[['condition_index', 'slope_1d', 'slope_3d', 'slope_7d']])
