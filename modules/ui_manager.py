import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 페이지네이션 초기화
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0
        
        # 2. 상단 버튼 영역 (업데이트/이전/다음)
        c1, c2, c3, c4 = st.columns([2, 1, 1, 6])
        with c1:
            if st.button("🔄 업데이트"): st.rerun()
        with c2:
            if st.button("◀"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
        with c3:
            if st.button("▶"):
                st.session_state.current_page += 1
                st.rerun()

        # 3. 카드 출력 영역
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        # 카드를 6개 컬럼으로 고정 배치
        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 가장 깔끔했던 카드 박스 디자인
                    st.markdown(f"""
                        <div style="border:1px solid #ddd; border-radius:10px; padding:10px; height:120px; background-color:white;">
                            <div style="font-size:10px; color:gray;">{game.get('display_date', '')}</div>
                            <div style="font-size:14px; font-weight:bold; margin:5px 0;">{game.get('display_time', '')}</div>
                            <div style="font-size:12px;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                            <div style="font-size:12px;">{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("상세보기", key=f"btn_{game.get('game_id', i)}"):
                        st.session_state.selected_game_id = game.get('game_id')
                        st.rerun()
