import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 상단 CSS (카드와 버튼 스타일 고정)
        st.markdown("""
            <style>
                .card-container { display: flex; align-items: center; justify-content: center; gap: 10px; }
                .game-card { 
                    width: 150px; height: 95px; border: 1px solid #ddd; border-radius: 10px;
                    padding: 8px; background: white; text-align: center; font-size: 11px;
                }
            </style>
        """, unsafe_allow_html=True)

        items_per_page = 6
        total_pages = max(1, (len(game_data_list) + items_per_page - 1) // items_per_page)
        if 'current_page' not in st.session_state: st.session_state.current_page = 0

        # 2. 양 끝에 버튼, 가운데에 카드를 배치하기 위한 컬럼 설정
        # [왼쪽 버튼(1) | 가운데 카드들(10) | 오른쪽 버튼(1)] 비율
        cols = st.columns([1, 10, 1])

        with cols[0]: # 왼쪽 끝: 이전 화살표
            if st.button("◀", key="prev"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()

        with cols[1]: # 중앙: 카드 6개 배치
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            start = st.session_state.current_page * items_per_page
            page_games = game_data_list[start:start + items_per_page]
            
            for game in page_games:
                st.markdown(f"""
                    <div class="game-card">
                        <div style="font-weight:bold; color:#666;">{game.get('display_date', '')}</div>
                        <div style="font-weight:bold; margin-top:5px;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                        <div>{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                    </div>
                """, unsafe_allow_html=True)
                # 클릭 시 상세 페이지로 이동하는 버튼을 별도 처리
                if st.button("보기", key=f"btn_{game.get('game_id')}"):
                    st.session_state.selected_game_id = game.get('game_id')
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with cols[2]: # 오른쪽 끝: 다음 화살표
            if st.button("▶", key="next"):
                if st.session_state.current_page < total_pages - 1:
                    st.session_state.current_page += 1
                    st.rerun()
