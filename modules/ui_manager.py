import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 완벽 고정 스타일 (기억하시는 그 가독성 디자인)
        st.markdown("""
            <style>
                .nav-wrapper { display: flex; align-items: center; justify-content: center; gap: 8px; }
                .card-final {
                    width: 130px; height: 90px;
                    border: 1px solid #e5e7eb; border-radius: 10px;
                    padding: 10px; background: white;
                    display: flex; flex-direction: column; justify-content: space-between;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.08);
                }
                .card-date { font-size: 9px; color: #6b7280; font-weight: bold; }
                .card-team { font-size: 12px; font-weight: 700; display: flex; justify-content: space-between; }
                .card-score { font-size: 12px; font-weight: 700; color: #111; }
            </style>
        """, unsafe_allow_html=True)

        items_per_page = 6
        start = st.session_state.get('current_page', 0) * items_per_page
        page_games = game_data_list[start:start + items_per_page]

        # 2. 버튼과 카드를 하나의 flex 컨테이너로 묶어 정렬 고정
        st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)
        
        # 이전 버튼
        if st.button("◀", key="prev_btn"):
            if st.session_state.get('current_page', 0) > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 카드 생성
        for game in page_games:
            # 텍스트 정보가 담긴 카드 영역
            card_html = f"""
                <div class="card-final">
                    <div class="card-date">{game.get('display_date', '종료')}</div>
                    <div class="card-team"><span>{game.get('away_name', 'AWY')}</span><span class="card-score">{game.get('away_score', 0)}</span></div>
                    <div class="card-team"><span>{game.get('home_name', 'HOM')}</span><span class="card-score">{game.get('home_score', 0)}</span></div>
                </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            # 카드 밑에 상세보기 버튼을 배치하여 레이아웃 방해 금지
            if st.button("상세보기", key=f"btn_{game.get('game_id')}"):
                st.session_state.selected_game_id = game.get('game_id')
                st.rerun()

        # 다음 버튼
        if st.button("▶", key="next_btn"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
