import streamlit as st

def render_game_navbar(game_data_list):
    # CSS: 화살표와 카드를 한 줄로 강제하고 버튼의 줄바꿈 속성을 제거
    st.markdown("""
        <style>
            /* 전체 네비게이션을 가로로 강제 정렬 */
            .nav-container { 
                display: flex !important; 
                flex-direction: row !important; 
                align-items: center !important; 
                justify-content: center !important; 
                gap: 10px !important;
            }
            /* 버튼들이 줄바꿈되지 않도록 인라인화 */
            div.stButton { display: inline-block; margin: 0; }
            
            /* 카드 디자인 */
            .game-card { 
                width: 140px; height: 90px; border: 1px solid #ddd; 
                border-radius: 8px; padding: 8px; background: white; 
                flex-shrink: 0; font-size: 11px;
            }
        </style>
    """, unsafe_allow_html=True)

    if 'current_page' not in st.session_state: st.session_state.current_page = 0
    
    # [핵심] 컨테이너 시작
    with st.container():
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        
        # 1. 왼쪽 화살표
        if st.button("◀", key="prev"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 2. 카드 6개
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for game in page_games:
            st.markdown(f"""
                <div class="game-card">
                    <div style="color:gray;">{game.get('display_date', '')}</div>
                    <div style="font-weight:bold;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                    <div>{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                </div>
            """, unsafe_allow_html=True)

        # 3. 오른쪽 화살표
        if st.button("▶", key="next"):
            st.session_state.current_page += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
