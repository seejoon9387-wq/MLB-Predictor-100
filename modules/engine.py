# [파일: engine.py]의 execute 부분 수정
def execute(self, data):
    # ... 이전 코드 생략 ...
    
    # 1. 모델 추론
    raw_prob = self.model.predict_proba(features_df)[0][1]
    
    # 2. 상성 보정 로직 통합
    # data에 포함된 투수/타자 정보를 기반으로 상성 가중치 산출
    matchup_adjustment = get_team_matchup_adjustment(data['lineup'], data['pitcher'])
    
    # 3. 보정된 승률 도출
    # raw_prob에 보정치를 더함 (0.01~0.03 정도의 미세 조정이 정확도 향상에 핵심)
    final_prob = raw_prob + matchup_adjustment
    
    return {
        "win_prob": round(final_prob * 100, 2),
        "raw_prob": round(raw_prob * 100, 2),
        "adjustment": round(matchup_adjustment * 100, 2)
    }
