import streamlit as st

class UIManager:
    @staticmethod
    def render_game_list(game_data_list, on_card_click):
        st.write("### 오늘의 경기 목록")
        for i, game in enumerate(game_data_list):
            time_str = f"{game.get('display_date')} {game.get('display_time')}"
            st.info(f"[{time_str}] {game.get('away_name')} vs {game.get('home_name')} | {game.get('away_score')} - {game.get('home_score')}")
            if st.button(f"경기 및 선수 기록 보기 ({i+1})", key=f"btn_{i}"):
                on_card_click(game)
