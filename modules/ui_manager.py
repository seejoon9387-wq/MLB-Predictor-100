import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # [디자인 고정 영역] 
        # 카드 가로 폭을 140px에서 180px로 확장하여 더 시원하게 만들었습니다.
        st.markdown("""
            <style>
                .custom-card { 
                    border: 1px solid #ddd; 
                    border-radius: 10px; 
                    padding: 10px; 
                    height: 120px; 
                    background-color: white;
                    text-align: center;
                    width: 180px; 
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # [배치 고정 영역] 
        # 화살표(col_prev)와 화살표(col_next)를 양 끝으로 밀고 중앙(col_cards)에 카드를 배치
        col_prev, col_cards, col_next = st.columns([1, 12, 1])
        
        with col_prev:
            st.markdown("<br><br>", unsafe_allow_html=True) # 카드 높이와 맞추기 위한 여백
            if st.button("◀"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1; st.rerun()

        with col_cards:
            start = st.session_state.current_page * 6
            page_games = game_data_list[start:start + 6]
            
            # 카드 6개를 나란히 배치
            sub_cols = st.columns(6)
            for i in range(6):
                with sub_cols[i]:
                    if i < len(page_games):
                        game = page_games[i]
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

        with col_next:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("▶"):
                st.session_state.current_page += 1; st.rerun()
