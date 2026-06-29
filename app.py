import streamlit as st
import statsapi
from modules.data_manager import DataManager
from modules.ui_manager import UIManager

# app.py의 중간에 이 내용을 추가하거나 수정하세요
from simulator import Simulator

# 경기 정보가 들어있는 game 변수가 있다고 가정
home = game['home_name'] 
away = game['away_name']

# 엔진 가동
win_prob = Simulator.calculate_win_probability(home, away)

# 화면 출력
st.write(f"### {away} vs {home}")
st.metric("홈팀 승리 예상 확률", f"{win_prob}%")

def analyze_win_probability(game):
    """기초적인 승률 예측 엔진 (현재는 안타 합계 기반)"""
    # 실제 모델로 발전시킬 자리
    return 50.0  # 기본값

def main():
    st.title("⚾ MLB 분석 엔진: 시각화 & 예측")

    # 1. 경기 목록 출력
    if 'games' not in st.session_state: st.session_state.games = fetch_data()
    
    def handle_click(game):
        DataManager.save_game(game)
        st.session_state.selected_game = game
        st.session_state.players = process_and_save_player_data(game['id'])
        st.rerun()

    UIManager.render_game_list(st.session_state.games, handle_click)

    # 2. 분석 엔진 구동부
    if 'selected_game' in st.session_state:
        st.divider()
        st.subheader("📊 경기 상세 분석")
        
        # 선수 데이터 시각화
        stats = DataManager.get_player_stats()
        if not stats.empty:
            # 해당 경기 선수들의 안타 수 그래프
            game_stats = stats[stats['game_id'] == st.session_state.selected_game['id']]
            if not game_stats.empty:
                st.bar_chart(game_stats.set_index('player_name')['hits'])
        
        # 승률 예측 결과
        prob = analyze_win_probability(st.session_state.selected_game)
        st.metric("승리 예측 확률", f"{prob}%")

if __name__ == "__main__":
    main()
