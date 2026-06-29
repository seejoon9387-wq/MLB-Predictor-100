import streamlit as st
import statsapi
from datetime import datetime
import pytz
from modules.ui_manager import UIManager

def fetch_data():
    try:
        # 오늘 날짜 확인 (2026-06-30 기준)
        today = datetime.now().strftime('%Y-%m-%d')
        raw_games = statsapi.schedule(date=today)
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
    except Exception as e:
        st.error(f"데이터 호출 중 오류 발생: {e}")
        return []

def main():
    st.title("⚾ MLB 실시간 경기 (한국 시간)")

    if 'games' not in st.session_state:
        st.session_state.games = fetch_data()

    if st.button("🔄 데이터 새로고침"):
        st.session_state.games = fetch_data()
        st.rerun()

    def handle_click(game):
        st.session_state.selected_game = game
        try:
            st.session_state.details = statsapi.game_data(game['id'])
        except:
            st.session_state.details = None
        st.rerun()

    UIManager.render_game_list(st.session_state.games, handle_click)

    if 'selected_game' in st.session_state:
        g = st.session_state.selected_game
        details = st.session_state.get('details')
        st.divider()
        st.subheader(f"📍 {g.get('away_name')} vs {g.get('home_name')} 상세 정보")
        if details:
            status = details['gameData']['status']['detailedState']
            weather = details['gameData']['weather'].get('condition', '정보 없음')
            st.write(f"경기 상황: {status}")
            st.write(f"날씨: {weather}")
        else:
            st.write("상세 정보 로딩 중...")

if __name__ == "__main__":
    main()
