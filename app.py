import streamlit as st
import statsapi
from datetime import datetime
import pytz
from modules.ui_manager import UIManager

def fetch_data():
    raw_games = statsapi.schedule(date=datetime.now().strftime('%Y-%m-%d'))
    games = []
    for g in raw_games:
        dt = datetime.strptime(g['game_datetime'], "%Y-%m-%dT%H:%M:%SZ")
        dt = dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Seoul'))
        games.append({
            "id": g['game_id'],
            "display_date": g['game_date'],
            "display_time": dt.strftime("%H:%M"),
            "away_name": g['away_name'],
            "away_score": g.get('away_score', 0),
            "home_name": g['home_name'],
            "home_score": g.get('home_score', 0)
        })
    return games

def fetch_details(game_id):
    # 경기 상세 데이터 (선발투수, 날씨 등) 호출
    box = statsapi.boxscore_data(game_id)
    info = statsapi.game_data(game_id)
    
    # 데이터 매핑
    weather = info['gameData']['weather'].get('condition', '정보 없음')
    away_pitcher = box['awayPitchers'][0] if box['awayPitchers'] else "미정"
    home_pitcher = box['homePitchers'][0] if box['homePitchers'] else "미정"
    
    return f"🌤 날씨: {weather} | ⚾ 선발: {away_pitcher} vs {home_pitcher}"

def main():
    st.title("⚾ MLB 실시간 경기")
    if 'games' not in st.session_state: st.session_state.games = fetch_data()

    def refresh():
        with st.spinner('정보 업데이트 중...'):
            st.session_state.games = fetch_data()
        st.rerun()

    def show_details(game):
        st.session_state.selected_game = game

    UIManager.render_game_navbar(st.session_state.games, refresh, show_details)

    if 'selected_game' in st.session_state:
        g = st.session_state.selected_game
        with st.expander(f"📍 {g['away_name']} vs {g['home_name']} 실시간 상세 정보", expanded=True):
            st.write(fetch_details(g['id']))

if __name__ == "__main__":
    main()
