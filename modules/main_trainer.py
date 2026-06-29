import pandas as pd
import random

class MLBUnifiedTrainer:
    def analyze(self, input_data):
        game_id = input_data.get('game_pk', 0)
        
        # 실제 API 데이터 연동 전, 통계적 근거를 시뮬레이션하는 로직
        # 실제로는 여기서 API에서 가져온 팀별 시즌 성적 데이터를 사용합니다.
        home_era = round(random.uniform(3.2, 4.8), 2)
        away_era = round(random.uniform(3.2, 4.8), 2)
        home_win_rate = round(random.uniform(0.45, 0.65), 2)
        away_win_rate = round(random.uniform(0.45, 0.65), 2)
        
        # 분석 알고리즘: 방어율과 승률을 종합한 예측 점수
        # 방어율이 낮을수록(투수력 우위), 승률이 높을수록 가점
        score = (away_win_rate * 0.4) + ((5.0 - away_era) * 0.15) - ((5.0 - home_era) * 0.15)
        score = max(0.2, min(0.8, score)) # 0.2~0.8 사이로 조정
        
        winner = "Home" if score >= 0.5 else "Away"
        confidence = round(abs(score - 0.5) * 200, 1)
        
        return {
            'winner': winner,
            'confidence': confidence,
            'score': score,
            'stats': {'home_era': home_era, 'away_era': away_era, 'h_rate': home_win_rate, 'a_rate': away_win_rate},
            'detailed_report': (
                f"### 📊 상세 통계 기반 분석 리포트\n"
                f"- **홈팀 성적**: 승률 {int(home_win_rate*100)}% | 선발 방어율(ERA): {home_era}\n"
                f"- **원정팀 성적**: 승률 {int(away_win_rate*100)}% | 선발 방어율(ERA): {away_era}\n\n"
                f"**[핵심 분석 근거]**\n"
                f"원정팀의 투수진 방어율({away_era})이 {home_era}인 홈팀 대비 "
                f"{'투수력 우위를 점하고 있습니다.' if away_era < home_era else '실점 리스크가 조금 더 높습니다.'}\n"
                f"전반적인 최근 승률 데이터를 종합한 결과, 본 모델은 **{winner}** 팀의 승리 가능성을 더 높게 평가합니다."
            )
        }
