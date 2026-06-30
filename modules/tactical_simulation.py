class TacticalSimulator:
    def __init__(self, manager_a_profile, manager_b_profile):
        self.manager_a = manager_a_profile # 예: {'bunt_rate': 0.2, 'bullpen_trust': 0.8}
        self.manager_b = manager_b_profile

    def simulate_clutch_advantage(self, situation_leverage):
        """
        상황 중요도(Leverage Index)에 따른 감독별 전술 기대치 차이를 산출
        """
        # 감독 성향 차이에 따른 승률 보정치 계산
        tactical_impact = (self.manager_a['bullpen_trust'] - self.manager_b['bullpen_trust']) * situation_leverage
        
        print(f"[Tactical Simulation] 레버리지 {situation_leverage} 상황에서의 전술 승률 보정치: {tactical_impact:.4f}")
        return tactical_impact

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    mgr_a = {'bunt_rate': 0.15, 'bullpen_trust': 0.9}
    mgr_b = {'bunt_rate': 0.35, 'bullpen_trust': 0.6}
    
    sim = TacticalSimulator(mgr_a, mgr_b)
    # 높은 레버리지 상황(2.5)에서의 시뮬레이션
    sim.simulate_clutch_advantage(2.5)
