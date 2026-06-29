import streamlit as st

class UIManager:
    @staticmethod
    def render_game_list(game_data_list, on_card_click):
        st.write("### 오늘의 경기 목록")
        for i, game in enumerate(game_data_list):
            # 변환된 한국 시간과 팀 정보를 표시
            time_str = f"{game.get('display_date', '')} {game.get('display_time', '')}"
            
            st.info(f"[{time_str}] {game.get('away_name', 'AWY')} vs {game.get('home_name', 'HOM')} | {game.get('away_score', 0)} - {game.get('home_score', 0)}")
            
            if st.button(f"경기 상세 보기 ({i+1})", key=f"btn_{i}"):
                on_card_click(game)
