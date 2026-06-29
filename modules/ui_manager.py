import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 스타일 설정 (가로 배열, 왼쪽 정렬)
        st.markdown("""
            <style>
                .nav-row { display: flex; align-items: center; justify-content: flex-start; gap: 10px; }
                .card-box {
                    width: 160px; height: 100px;
                    border: 1px solid #e5e7eb; border-radius: 12px;
                    padding: 12px; background: white;
                    display: flex; flex-direction: column; justify-content: space-between;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    flex-shrink: 0;
                }
            </style>
        """, unsafe_allow_html=True)

        items_per_page = 6
        total_pages = max(1, (len(game_data_list) + items_per_page - 1) // items_per_page)
        if 'current_page' not in st.session_state: st.session_state.current_page = 0

        # 2. 컨테이너 시작
        st.markdown('<div class="nav-row">', unsafe_allow_html=True)
        
        # 이전 화살표 (왼쪽)
        if st.button("◀", key="prev"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 3. 카드 출력 (페이지에 해당하는 데이터만)
        start = st.session_state.current_page * items_per_page
        page_games = game_data_list[start:start + items_per_page]

        for game in page_games:
            # 카드와 버튼이 일렬로 보이도록 배치
            st.markdown(f"""
                <div class="card-box">
                    <div style="font-size: 10px; color: #6b7280; font-weight: bold;">{game.get('display_date', '')}</div>
                    <div style="font-size: 13px; font-weight: 700; display: flex; justify-content: space-between;">
                        <span>{game.get('away_name', 'AWY')}</span> <span>{game.get('away_score', 0)}</span>
                    </div>
                    <div style="font-size: 13px; font-weight: 700; display: flex; justify-content: space-between;">
                        <span>{game.get('home_name', 'HOM')}</span> <span>{game.get('home_score', 0)}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # 상세보기 버튼을 카드마다 연결
            if st.button("보기", key=f"btn_{game.get('game_id')}"):
                st.session_state.selected_game_id = game.get('game_id')
                st.rerun()

        # 다음 화살표 (오른쪽)
        if st.button("▶", key="next"):
            if st.session_state.current_page < total_pages - 1:
                st.session_state.current_page += 1
                st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
