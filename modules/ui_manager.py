import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 스타일 정의: 무조건 가로 정렬(Flex)
        st.markdown("""
            <style>
                .navbar-outer { display: flex; align-items: center; justify-content: space-between; width: 100%; gap: 10px; }
                .cards-inner { display: flex; flex-direction: row; gap: 15px; justify-content: center; }
                .card-box { 
                    width: 150px; height: 90px; border: 1px solid #ddd; border-radius: 8px; 
                    padding: 8px; background: white; flex-shrink: 0;
                    font-size: 11px; display: flex; flex-direction: column; justify-content: space-between;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 메인 컨테이너 시작
        st.markdown('<div class="navbar-outer">', unsafe_allow_html=True)
        
        # 3. 화살표 (st.button 대신 HTML 버튼을 쓰면 옆으로 배치됨)
        # 편의상 st.button을 사용하되, 가로 배치를 방해하지 않게 div로 묶음
        if st.button("◀", key="prev"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 4. 카드 영역
        st.markdown('<div class="cards-inner">', unsafe_allow_html=True)
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for game in page_games:
            st.markdown(f"""
                <div class="card-box">
                    <div style="color:gray;">{game.get('display_date', '')}</div>
                    <div style="font-weight:bold;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                    <div>{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 5. 오른쪽 화살표
        if st.button("▶", key="next"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
