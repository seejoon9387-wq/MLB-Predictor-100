import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list, on_card_click):
        start = st.session_state.get('current_page', 0) * 6
        page_games = game_data_list[start:start + 6]
        
        # 6개 컬럼 생성
        cols = st.columns(6)
        
        for i, col in enumerate(cols):
            with col:
                if i < len(page_games):
                    game = page_games[i]
                    # 버튼을 카드 상단에 명시적으로 배치 (이제 사라지지 않습니다)
                    if st.button("경기 상세 선택", key=f"btn_{i}"):
                        on_card_click(game)
                    
                    # 카드 내용 출력
                    st.write(f"**{game['away_name']}**")
                    st.write(f"{game['away_score']} : {game['home_score']}")
                    st.write(f"**{game['home_name']}**")
                else:
                    st.empty()
