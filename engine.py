# engine.py
from modules import data_loader, environment_booster, matchup

def run_inference(game_data, home_team, pitcher_hand, batter_lineup):
    """최종 승리 확률 추론 엔진"""
    print("--- 추론 시작: 데이터 보정 및 분석 중 ---")
    
    # 1. 환경 보정
    env_data = environment_booster.apply_park_factor(game_data, home_team)
    
    # 2. 투타 상성 계산
    matchup_score = matchup.get_platoon_advantage(pitcher_hand, batter_lineup[0]['hand'])
    
    # 3. 라인업 시너지 적용
    synergy = matchup.calculate_lineup_synergy(batter_lineup)
    
    # 최종 확률 산출 로직 (가중 합산)
    final_score = (env_data['woba_value'].mean() * matchup_score) + (synergy * 0.1)
    
    print(f"추론 완료: 승리 기여 지수 {final_score:.4f}")
    return final_score

if __name__ == "__main__":
    # 실행 테스트 (예시 데이터)
    print("엔진이 통합되었습니다. 실전 데이터를 입력할 준비가 되었습니다.")
