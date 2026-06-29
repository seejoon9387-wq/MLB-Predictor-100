import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 페이지 초기화
        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 8개의 컬럼을 생성합니다: [◀][카드1][카드2][카드3][카드4][카드5][카드6][▶]
        # 각 카드에 적절한 비율을 할당하여 줄바꿈을 방지합니다.
        cols = st.columns([0.5, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 0.5])
        
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]

        # 1. 왼쪽 화살표
        with cols[0]:
            if st.button("◀", key="prev"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()

        # 2. 카드 6개 배치
        for i in range(6):
            with cols[i+1]:
                if i < len(page_games):
                    game = page_games[i]
                    # 카드 스타일 (CSS를 최소화하고 스트림릿 내장 마크다운만 사용)
                    st.markdown(f"""
                        <div style="border:1px solid #ccc; border-radius:8px; padding:5px; text-align:center; font-size:10px;">
                            <div style="color:gray;">{game.get('display_date', '')}</div>
                            <div style="font-weight:bold;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                            <div>{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("") # 빈 공간 유지

        # 3. 오른쪽 화살표
        with cols[7]:
            if st.button("▶", key="next"):
                st.session_state.current_page += 1
                st.rerun()
