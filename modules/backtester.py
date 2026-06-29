# modules/backtester.py
import pandas as pd
import numpy as np

def run_backtest(df, threshold=0.05):
    """
    백테스팅 수행: inefficiency_score에 따른 전략 수익률 계산
    """
    # 전략: 모델 승률 > 시장 승률 + threshold 인 경우 베팅
    df['bet_signal'] = np.where(df['inefficiency_score'] > threshold, 1, 0)
    
    # 실제 결과와 비교
    df['profit'] = np.where(df['bet_signal'] == 1, 
                            np.where(df['is_home_win'] == 1, (df['current_home_odds'] - 1), -1), 
                            0)
    
    # 성과 지표 계산
    total_bets = df['bet_signal'].sum()
    win_rate = df[df['bet_signal'] == 1]['is_home_win'].mean()
    total_profit = df['profit'].sum()
    
    return {
        "총 베팅 횟수": total_bets,
        "전략 승률": f"{win_rate:.2%}",
        "누적 수익(단위: 유닛)": f"{total_profit:.2f}",
        "베팅당 기대 수익": f"{(total_profit / total_bets):.4f}" if total_bets > 0 else 0
    }
