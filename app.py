import streamlit as st
import statsapi
from modules.ui_manager import UIManager

def show_game_details(game_id):
    st.subheader("⚾ 경기 상세 정보")
    # statsapi로 상세 데이터 조회
    data = statsapi.game_data(game_id)
    
    # 1. 선발 투수
    st.write(f"**선발 투수:** {data['lineups']['home'][0]} vs {data['lineups']['away'][0]}")
    
    # 2. 경기장 정보
    st.write(f"**경기장:** {data['venue']['name']}")
    
    # 3. 날씨 정보
    weather = data.get('weather', {})
    st.write(f"**날씨:** {weather.get('condition', '정보없음')} / 온도: {weather.get('temp', 'N/A')}")
    
    # 4. 부상자 및 기타 정보 (statsapi의 game_data는 매우 상세합니다)
    with st.expander("라인업 및 추가 정보 확인"):
        st.json(data['lineups']) # 상세 라인업 출력

def main():
    st.title("⚾ MLB 실시간 경기 센터")
    
    # 게임 선택 상태 관리
    if 'selected_game_id' in st.session_state:
        if st.button("⬅ 목록으로 돌아가기"):
            del st.session_state.selected_game_id
            st.rerun()
        show_game_details(st.session_state.selected_game_id)
    else:
        games = get_filtered_mlb_data()
        UIManager.render_game_navbar(games)

# ... 나머지 함수들 ...
