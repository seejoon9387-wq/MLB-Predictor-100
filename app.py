import streamlit as st
import statsapi
from datetime import datetime
import pytz
from modules.ui_manager import UIManager

def fetch_data():
    try:
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
    except:
        return []

def main():
    st.title("⚾ MLB 실시간 경기")
    
    # 데이터 초기화 보장
    if 'games' not in st.session_state:
        st.session_state.games = fetch_data()

    if st.button("🔄 실시간 업데이트"):
        with st.spinner('정보 업데이트 중...'):
            st.session_state.games = fetch_data()
        st.rerun()

    # 상세 정보 클릭 이벤트
    def handle_card_click(game):
        st.session_state.selected_game = game

    # UI 렌더링 호출
    UIManager.render_game_navbar(st.session_state.games, handle_card_click)

    # 선택된 게임 상세 정보 표시
    if 'selected_game' in st.session_state:
        g = st.session_state.selected_game
        st.divider()
        st.subheader(f"📍 {g['away_name']} vs {g['home_name']} 상세 정보")
        # 상세 데이터 가져오기 로직 (예외 처리 추가)
        try:
            info = statsapi.game_data(g['id'])
            weather = info['gameData']['weather'].get('condition', '정보없음')
            st.write(f"🌤 날씨: {weather}")
        except:
            st.write("상세 정보를 불러올 수 없습니다.")

if __name__ == "__main__":
    main()
