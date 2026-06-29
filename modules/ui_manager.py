import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # [디자인 고정 영역] 이 스타일은 절대 수정하지 않습니다.
        st.markdown("""
            <style>
                .custom-card { 
                    border: 1px solid #ddd; 
                    border-radius: 10px; 
                    padding: 10px; 
                    height: 120px; 
                    background-color: white;
                    text-align: center;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # [배치 고정 영역] 상단 업데이트 및 이전/다음 버튼 위치 고정
        col_up, col_prev, col_next, col_empty = st.columns([2, 1, 1, 6])
        with col_up:
            if st.button("🔄 업데이트"): st.rerun()
        with col_prev:
            if st.button("◀"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1; st.rerun()
        with col_next:
            if st.button("▶"):
                st.session_state.current_page += 1; st.rerun()

        # [카드 배열 고정] 6개 컬럼 고정 배치
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 고정된 클래스 적용
                    st.markdown(f"""
                        <div class="custom-card">
                            <div style="font-size:10px; color:gray;">{game.get('display_date', '')}</div>
                            <div style="font-size:14px; font-weight:bold; margin:5px 0;">{game.get('display_time', '')}</div>
                            <div style="font-size:12px;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                            <div style="font-size:12px;">{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("상세보기", key=f"btn_{game.get('game_id', i)}"):
                        st.session_state.selected_game_id = game.get('game_id')
                        st.rerun()
