import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 전체를 상단 중앙으로 배치하기 위한 컨테이너 설정
        st.markdown("""
            <style>
                /* 전체 페이지 상단 여백 제거 */
                .block-container { padding-top: 1rem; }
                /* 카드를 가로로 넓게 설정 */
                .card-wide {
                    width: 95%; 
                    height: 180px;
                    border: 1px solid #d1d5db;
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    background: white;
                    margin: 0 auto;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
            </style>
        """, unsafe_allow_html=True)

        items_per_page = 6
        start = st.session_state.get('current_page', 0) * items_per_page
        page_games = game_data_list[start:start + items_per_page]

        # 1. 상단 화살표 (가운데 정렬)
        c1, c2, c3 = st.columns([1, 8, 1])
        with c1:
            if st.button("◀ 이전"):
                if st.session_state.get('current_page', 0) > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
        with c3:
            if st.button("다음 ▶"):
                st.session_state.current_page = st.session_state.get('current_page', 0) + 1
                st.rerun()

        # 2. 카드 배치 (6개 칼럼을 가로로 길게 확장)
        cols = st.columns(6) 
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 카드 내부 텍스트 및 디자인
                    st.markdown(f"""
                        <div class="card-wide">
                            <div style="font-size: 11px; color: #6b7280; font-weight: bold;">{game.get('display_date', '')}</div>
                            <div style="font-size: 18px; font-weight: 800; color: #dc2626; margin: 10px 0;">{game.get('display_time', '')}</div>
                            <div style="font-size: 14px; font-weight: 700; margin-bottom: 5px;">{game.get('away_name', 'AWAY')}</div>
                            <div style="font-size: 14px; font-weight: 700;">{game.get('home_name', 'HOME')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("상세보기", key=f"btn_{game.get('game_id', i)}"):
                        st.session_state.selected_game_id = game.get('game_id')
                        st.rerun()
                else:
                    st.write("")
