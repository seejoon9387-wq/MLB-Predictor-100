# data_loader.py
from modules.bayesian_updater import get_bayesian_win_prob

def load_data():
    # ... (데이터 로드) ...
    # 팀별 베이지안 승률 계산 (사전 정보 비중은 초기 20)
    df['bayesian_win_rate'] = df.apply(
        lambda x: get_bayesian_win_prob(x['team_wins'], x['team_games']), axis=1
    )
    # ... (기타 세이버메트릭스 엔진 실행) ...
    return df
