import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 디자인 고정 (카드를 오른쪽으로 더 넓게, 가로 배열)
        st.markdown("""
            <style>
                .main-row { display: flex; align-items: center; justify-content: flex-start; gap: 15px; overflow-x: auto; padding-bottom: 20px; }
                .card-item {
                    width: 160px; height: 100px; /* 오른쪽으로 더 크게 확장 */
                    border: 1px solid #e5e7eb; border-radius: 12px;
                    padding: 12px; background: white;
                    display: flex; flex-direction: column; justify-content: space-between;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    flex-shrink: 0;
                }
                .card-date { font-size: 10px; color: #6b7280; font-weight: bold; }
                .team-line { display: flex; justify-content: space-between; font-size: 13px; font-weight: 700; }
            </style>
        """, unsafe_allow_html=True)

        items_per_page = 6
        start = st.session_state.get('current_page', 0) * items_per_page
        page_games = game_data_list[start:start + items_per_page]

        # 2. 버튼과 카드를 하나의 flex 행(Row)으로 배치
        st.markdown('<div class="main-row">', unsafe_allow_html=True)
        
        # 이전 버튼
        if st.button("◀", key="prev"):
            if st.session_state.get('current_page', 0) > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 카드 생성
        for game in page_games:
            # 상세보기 버튼을 카드 안의 요소로 포함시켜 배치 오류 원천 차단
            if st.button(f"보기", key=f"btn_{game.get('game_id')}"):
                st.session_state.selected_game_id = game.get('game_id')
                st.rerun()
            
            st.markdown(f"""
                <div class="card-item">
                    <div class="card-date">{game.get('display_date', '종료')}</div>
                    <div class="team-line"><span>{game.get('away_name', 'AWY')}</span><span>{game.get('away_score', 0)}</span></div>
                    <div class="team-line"><span>{game.get('home_name', 'HOM')}</span><span>{game.get('home_score', 0)}</span></div>
                </div>
            """, unsafe_allow_html=True)

        # 다음 버튼
        if st.button("▶", key="next"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
