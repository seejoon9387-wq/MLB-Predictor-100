import streamlit as st

class UIManager:
    @staticmethod
    def render_game_list(game_data_list, on_card_click):
        st.write("### 오늘의 경기 목록")
        # 리스트 형태로 단순 출력
        for i, game in enumerate(game_data_list):
            # 경기 정보를 텍스트로 명확히 표시
            st.write(f"경기: {game.get('away_name')} vs {game.get('home_name')}")
            st.write(f"점수: {game.get('away_score')} : {game.get('home_score')}")
            
            # 상세보기 버튼
            if st.button(f"상세 정보 보기 ({i})", key=f"btn_{i}"):
                on_card_click(game)
            st.divider()
