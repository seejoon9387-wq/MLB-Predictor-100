import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 디자인을 위해 간단한 격자형 카드로 출력
        cols = st.columns(3) # 3개씩 배치
        for i, game in enumerate(game_data_list):
            with cols[i % 3]:
                st.markdown(f"""
                    <div style="border:1px solid #ddd; border-radius:10px; padding:15px; margin:5px; background-color:#f9f9f9;">
                        <h4 style="margin:0;">{game.get('away_name')} vs {game.get('home_name')}</h4>
                        <p style="margin:5px 0;">{game.get('display_date', '')} {game.get('display_time', '')}</p>
                        <p style="margin:5px 0;">점수: {game.get('away_score')} - {game.get('home_score')}</p>
                    </div>
                """, unsafe_allow_html=True)
                # 상세보기 버튼
                if st.button(f"상세보기 {game['game_id']}", key=f"btn_{game['game_id']}"):
                    st.session_state.selected_game_id = game['game_id']
                    st.rerun()
