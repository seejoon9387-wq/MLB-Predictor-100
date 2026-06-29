import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 스타일 설정: 버튼과 카드를 '인라인'으로 배치
        st.markdown("""
            <style>
                .nav-row { display: flex; align-items: center; justify-content: center; gap: 15px; }
                .card-item {
                    display: flex; flex-direction: column; align-items: center;
                    width: 140px; text-align: center;
                }
                .game-box {
                    border: 1px solid #ddd; border-radius: 10px; padding: 10px;
                    width: 140px; height: 90px; background: white;
                    font-size: 11px; margin-bottom: 5px;
                }
            </style>
        """, unsafe_allow_html=True)

        items_per_page = 6
        total_pages = max(1, (len(game_data_list) + items_per_page - 1) // items_per_page)
        if 'current_page' not in st.session_state: st.session_state.current_page = 0

        # 2. 양 끝 화살표와 중앙 컨테이너
        cols = st.columns([1, 10, 1])

        with cols[0]:
            if st.button("◀", key="prev"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()

        with cols[1]:
            st.markdown('<div class="nav-row">', unsafe_allow_html=True)
            start = st.session_state.current_page * items_per_page
            page_games = game_data_list[start:start + items_per_page]
            
            for game in page_games:
                # 카드와 버튼을 하나의 div(card-item)로 묶어서 가로로만 배치
                st.markdown(f"""
                    <div class="card-item">
                        <div class="game-box">
                            <div style="font-weight:bold;">{game.get('display_date', '')}</div>
                            <div style="display:flex; justify-content:space-between;"><span>{game.get('away_name', 'AWY')}</span> <b>{game.get('away_score', 0)}</b></div>
                            <div style="display:flex; justify-content:space-between;"><span>{game.get('home_name', 'HOM')}</span> <b>{game.get('home_score', 0)}</b></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                # 상세보기 버튼은 이제 세로로 밀려나지 않도록 카드 하단에 고정
                if st.button("보기", key=f"btn_{game.get('game_id')}"):
                    st.session_state.selected_game_id = game.get('game_id')
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with cols[2]:
            if st.button("▶", key="next"):
                if st.session_state.current_page < total_pages - 1:
                    st.session_state.current_page += 1
                    st.rerun()
