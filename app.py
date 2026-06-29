import streamlit as st
import statsapi
from datetime import datetime
import pytz
from modules.ui_manager import UIManager
from modules.data_manager import DataManager

def fetch_data():
    try:
        raw_games = statsapi.schedule(date=datetime.now().strftime('%Y-%m-%d'))
        games = []
        seoul_tz = pytz.timezone('Asia/Seoul')
        for g in raw_games:
            dt_utc = datetime.strptime(g['game_datetime'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
            dt_seoul = dt_utc.astimezone(seoul_tz)
            games.append({
                "id": g['game_id'],
                "display_date": dt_seoul.strftime("%Y-%m-%d"),
                "display_time": dt_seoul.strftime("%H:%M"),
                "away_name": g['away_name'],
                "away_score": g.get('away_score', 0),
                "home_name": g['home_name'],
                "home_score": g.get('home_score', 0)
            })
        return games
    except: return []

def process_and_save_player_data(game_id):
    try:
        box = statsapi.boxscore_data(game_id)
        player_stats = []
        # 원정팀 선수들 기록 추출
        for p_id in box['away']['batters']:
            p = box['away']['players']['ID' + str(p_id)]
            player_stats.append({
                'game_id': game_id, 'player_name': p['fullName'],
                'hits': p['stats']['batting'].get('hits', 0),
                'home_runs': p['stats']['batting'].get('homeRuns', 0)
            })
        DataManager.save_player_stats(player_stats)
        return player_stats
    except: return []

def main():
    st.title("⚾ MLB 분석 엔진: 데이터 수집")
    if 'games' not in st.session_state: st.session_state.games = fetch_data()

    def handle_click(game):
        DataManager.save_game(game) # 경기 정보 저장
        st.session_state.selected_game = game
        st.session_state.players = process_and_save_player_data(game['id']) # 선수 기록 저장
        st.rerun()

    UIManager.render_game_list(st.session_state.games, handle_click)

    if 'selected_game' in st.session_state:
        st.divider()
        st.subheader(f"{st.session_state.selected_game['away_name']} 선수 기록 저장 완료")
        st.write(f"총 {len(st.session_state.players)}명의 선수 데이터가 기록되었습니다.")

if __name__ == "__main__":
    main()
