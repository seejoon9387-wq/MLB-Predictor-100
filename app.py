import streamlit as st
import statsapi
from datetime import datetime
import pytz
from modules.ui_manager import UIManager

def fetch_data():
    # 데이터 호출 시 에러 발생 방지를 위해 예외 처리 추가
    try:
        raw_games = statsapi.schedule(date=datetime.now().strftime('%Y-%m-%d'))
        games = []
        for g in raw_games:
            # 날짜 변환 로직
            dt = datetime.strptime(g['game_datetime'], "%Y-%m-%dT%H:%M:%SZ")
            dt = dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Seoul'))
            games.append({
                "id": g['game_id'],
                "away_name": g['away_name'],
                "away_score": g.get('away_score', 0),
                "home_name": g['home_name'],
                "home_score": g.get('home_score', 0)
            })
        return games
    except Exception as e:
        st.error(f"데이터를 불러오는 중 에러 발생: {e}")
        return []

def main():
    st.title("⚾ MLB 실시간 경기 데이터")

    if 'games' not in st.session_state:
        st.session_state.games = fetch_data()

    if st.button("🔄 데이터 새로고침"):
        st.session_state.games = fetch_data()
        st.rerun()

    # 데이터 호출 확인
    if not st.session_state.games:
        st.warning("오늘 경기 데이터가 없습니다.")
        return

    # 리스트 출력
    def handle_click(game):
        st.session_state.selected_game = game
        try:
            st.session_state.details = statsapi.game_data(game['id'])
        except Exception as e:
            st.session_state.details = None
            st.error("상세 정보 호출 실패")
        st.rerun()

    UIManager.render_game_list(st.session_state.games, handle_click)

    # 상세 정보 출력
    if 'selected_game' in st.session_state:
        st.divider()
        st.subheader("상세 정보")
        details = st.session_state.get('details')
        if details:
            st.write(f"경기 상황: {details['gameData']['status']['detailedState']}")
            st.write(f"날씨: {details['gameData']['weather'].get('condition', '정보 없음')}")
        else:
            st.write("상세 정보를 불러오는 중입니다.")

if __name__ == "__main__":
    main()
