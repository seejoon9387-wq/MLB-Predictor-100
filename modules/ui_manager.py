import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 디자인 고정 및 겹침 방지 CSS
        st.markdown("""
            <style>
                .navbar-box { display: flex; align-items: center; justify-content: space-between; width: 100%; gap: 15px; }
                .cards-row { 
                    display: flex; flex-direction: row; flex-wrap: nowrap; 
                    justify-content: center; gap: 15px; overflow-x: auto; 
                }
                .custom-card { 
                    border: 1px solid #ddd; border-radius: 10px; padding: 10px; 
                    background-color: white; text-align: center;
                    width: 160px; height: 110px; flex-shrink: 0;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 양 끝 화살표와 중앙 카드 영역 배치를 위한 컨테이너
        st.markdown('<div class="navbar-box">', unsafe_allow_html=True)
        
        # 왼쪽 화살표
        if st.button("◀", key="prev"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1; st.rerun()

        # 3. 카드 영역 (가로 일렬 배치 강제)
        st.markdown('<div class="cards-row">', unsafe_allow_html=True)
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for game in page_games:
            st.markdown(f"""
                <div class="custom-card">
                    <div style="font-size:9px; color:gray;">{game.get('display_date', '')}</div>
                    <div style="font-size:12px; font-weight:bold; margin:5px 0;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                    <div style="font-size:12px;">{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                </div>
            """, unsafe_allow_html=True)
            # 버튼은 카드 안으로 넣기 어렵기 때문에 카드 바로 아래로 배치하거나 생략 권장
            if st.button("보기", key=f"btn_{game.get('game_id', i)}"):
                st.session_state.selected_game_id = game.get('game_id')
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # 오른쪽 화살표
        if st.button("▶", key="next"):
            st.session_state.current_page += 1; st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
